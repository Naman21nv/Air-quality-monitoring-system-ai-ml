import requests
from flask import Flask, request, jsonify, make_response
import joblib
import numpy as np
import pandas as pd
import os
from datetime import datetime
from tensorflow.keras.models import load_model
from flask_cors import CORS
from functools import wraps
from flask import current_app
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =======================
# CONFIGURATION
# =======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "corrected_precautionary_data.csv")
MODEL_FILE = os.path.join(BASE_DIR, "pollution_cnn_lstm_model.h5")
SCALER_FILE = os.path.join(BASE_DIR, "pollution_scaler.pkl")
LABEL_ENCODER_FILE = os.path.join(BASE_DIR, "pollution_label_encoder.pkl")

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI')
if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable not set. Please check your .env file.")
MONGODB_DB = "air_quality_db"
MONGODB_COLLECTION = "aqi_readings"

app = Flask(__name__)

# =======================
# MONGODB CONNECTION
# =======================
mongo_client = None
db = None
aqi_collection = None

try:
    print("Connecting to MongoDB Atlas...")
    mongo_client = MongoClient(
        MONGODB_URI, 
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
        socketTimeoutMS=10000
    )
    # Test the connection
    mongo_client.admin.command('ping')
    db = mongo_client[MONGODB_DB]
    aqi_collection = db[MONGODB_COLLECTION]
    print("✓ Successfully connected to MongoDB!")
    print(f"  Database: {MONGODB_DB}, Collection: {MONGODB_COLLECTION}")
except ConnectionFailure as e:
    print(f"✗ Failed to connect to MongoDB: {e}")
    print("  Application will continue without MongoDB support")
except Exception as e:
    print(f"✗ MongoDB connection error: {e}")
    print("  Application will continue without MongoDB support")

def add_cors_headers(response):
    # Allow requests from any origin during development
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Max-Age'] = '3600'
    return response

# CORS setup with permissive settings for development
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False
    }
})

@app.after_request
def after_request(response):
    return add_cors_headers(response)

# Handle OPTIONS requests globally
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        add_cors_headers(response)
        return response

@app.route('/')
def home():
    response = jsonify({"message": "Air Quality Monitoring API is running"})
    return response, 200

@app.route('/api/aqi', methods=['POST', 'OPTIONS'])
def save_aqi():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Log the received data for debugging
        print("Received AQI data:", data)
        
        # Send a proper response with the received data
        return jsonify({
            "message": "AQI data received successfully",
            "data": data
        }), 200
    except Exception as e:
        print("Error in /api/aqi endpoint:", str(e))
        return jsonify({"error": str(e)}), 400

# =======================
# LOAD MODEL & DATA
# =======================
try:
    model = load_model(MODEL_FILE)
    scaler = joblib.load(SCALER_FILE)
    label_encoder = joblib.load(LABEL_ENCODER_FILE)
    df = pd.read_csv(DATA_FILE)

    # Features that model & dataset share
    features = ["CO", "NO2", "PM2.5", "SO2"]

    print("Model and preprocessors loaded successfully.")
except Exception as e:
    print(f"Error loading model or preprocessors: {e}")
    model = None
    scaler = None
    label_encoder = None
    df = None


@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    if model is None or scaler is None or label_encoder is None or df is None:
        return jsonify({"error": "Model, preprocessors, or data not loaded."}), 500

    try:
        # =======================
        # STEP 1: Collect Inputs
        # =======================
        data = request.json
        
        co = float(data.get("CO", 0))
        no2 = float(data.get("NO2", 0))
        pm25 = float(data.get("PM2.5", 0))
        so2 = float(data.get("SO2", 0))
        city_name = data.get("city_name", "Unknown City")

        print(f"\n=== PREDICTION REQUEST ===")
        print(f"City: {city_name}")
        print(f"CO: {co}, NO2: {no2}, PM2.5: {pm25}, SO2: {so2}")
        
        prediction_response = predict_logic(co, no2, pm25, so2, city_name)
        
        print(f"Prediction AQI: {prediction_response.get('aqi')}")
        print(f"=========================\n")
        
        # =======================
        # STEP 2: Store to MongoDB
        # =======================
        if aqi_collection is not None:
            try:
                mongo_document = {
                    "city": city_name,
                    "timestamp": datetime.utcnow(),
                    "pollutants": {
                        "CO": co,
                        "NO2": no2,
                        "PM2.5": pm25,
                        "SO2": so2
                    },
                    "prediction": {
                        "aqi": prediction_response.get('aqi'),
                        "source": prediction_response.get('source'),
                        "health_impact": prediction_response.get('health_impact'),
                        "precautionary_measures": prediction_response.get('precautionary_measures')
                    }
                }
                result = aqi_collection.insert_one(mongo_document)
                print(f"✓ Data stored to MongoDB with ID: {result.inserted_id}")
                
                # =======================
                # STEP 3: Auto-update Dataset from MongoDB
                # =======================
                try:
                    # Append this new reading to the CSV dataset
                    new_row = {
                        'CO': co,
                        'NO2': no2,
                        'PM2.5': pm25,
                        'SO2': so2,
                        'AQI': prediction_response.get('aqi'),
                        'health_impact': prediction_response.get('health_impact'),
                        'Precautionary_Measures': prediction_response.get('precautionary_measures')
                    }
                    
                    # Read existing dataset
                    dataset_df = pd.read_csv(DATA_FILE)
                    
                    # Append new row
                    dataset_df = pd.concat([dataset_df, pd.DataFrame([new_row])], ignore_index=True)
                    
                    # Save updated dataset
                    dataset_df.to_csv(DATA_FILE, index=False)
                    print(f"✓ Dataset updated: {DATA_FILE}")
                    
                except Exception as csv_error:
                    print(f"Warning: Could not update CSV dataset: {csv_error}")
                    
            except Exception as mongo_error:
                print(f"MongoDB storage error: {mongo_error}")
                # Continue even if MongoDB fails
        
        return jsonify(prediction_response), 200

    except Exception as e:
        # Return a general, but informative, error for the frontend
        return jsonify({"error": f"An unexpected error occurred during prediction: {str(e)}"}), 500



@app.route('/get_aqi_data', methods=['POST'])
def get_aqi_data():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    try:
        data = request.json
        city = data.get("city")
        if not city:
            return jsonify({"error": "City not provided"}), 400

        token = os.environ.get("WAQI_TOKEN")
        if not token:
            return jsonify({"error": "WAQI_TOKEN environment variable not set. Please get a token from https://aqicn.org/data-platform/token/"}), 500

        # Make request to WAQI API
        waqi_url = f"https://api.waqi.info/feed/{city}/?token={token}"
        
        try:
            waqi_response = requests.get(waqi_url, timeout=10)
            waqi_response.raise_for_status()  # Raise an exception for bad status codes
            waqi_data = waqi_response.json()
        except requests.exceptions.Timeout:
            return jsonify({"error": "Request to WAQI API timed out."}), 504
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"An error occurred with WAQI API: {e}"}), 500

        if waqi_data.get("status") != "ok":
            error_details = waqi_data.get("data", "No details provided")
            if error_details == "Invalid key":
                return jsonify({"error": "Invalid WAQI_TOKEN. Please get a new token from https://aqicn.org/data-platform/token/"}), 401
            return jsonify({"error": f"Failed to fetch data from WAQI API: {error_details}"}), 500

        # Extract pollutant data
        iaqi = waqi_data.get("data", {}).get("iaqi", {})
        co = iaqi.get("co", {}).get("v", 0)
        no2 = iaqi.get("no2", {}).get("v", 0)
        pm25 = iaqi.get("pm25", {}).get("v", 0)
        so2 = iaqi.get("so2", {}).get("v",0)

        # Call prediction logic
        prediction_response = predict_logic(co, no2, pm25, so2, city)

        # Combine responses
        response = {
            "waqi_data": waqi_data.get("data"),
            "prediction": prediction_response
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def predict_logic(co, no2, pm25, so2, city_name):
    if model is None or scaler is None or label_encoder is None or df is None:
        return {"error": "Model, preprocessors, or data not loaded."}

    try:
        # =======================
        # STEP 2: ML Prediction
        # =======================
        user_input = np.array([[co, no2, pm25, so2]])

        try:
            user_scaled = scaler.transform(user_input)
        except Exception as e:
            return {"error": f"Scaler transform failed: {str(e)}"}

        user_scaled = user_scaled.reshape((1, user_scaled.shape[1], 1))

        pred_source_idx = np.argmax(model.predict(user_scaled), axis=1)[0]
        pred_source = label_encoder.inverse_transform([pred_source_idx])[0]

        # =======================
        # STEP 3: Closest Row Lookup from Dataset
        # =======================
        try:
            closest_row = df.iloc[((df[features] - user_input) ** 2).sum(axis=1).idxmin()]
        except Exception as e:
            return {"error": f"Closest row lookup failed: {str(e)}"}

        pred_health = str(closest_row.get("health_impact", "N/A"))
        pred_measures = str(closest_row.get("Precautionary_Measures", "N/A"))

        try:
            pred_aqi = float(closest_row["AQI"])
        except Exception:
            pred_aqi = str(closest_row["AQI"])

        # =======================
        # STEP 4: Response
        # =======================
        response = {
            "source": pred_source,
            "health_impact": pred_health,
            "precautionary_measures": pred_measures,
            "aqi": pred_aqi,
            "city": city_name # Add city name to the response for front-end clarity
        }

        return response

    except Exception as e:
        # Return a general, but informative, error for the frontend
        return {"error": f"An unexpected error occurred during prediction: {str(e)}"}

# =======================
# MONGODB DATA ENDPOINTS
# =======================

@app.route('/api/historical-data', methods=['GET'])
def get_historical_data():
    """Get historical AQI data from MongoDB"""
    if aqi_collection is None:
        return jsonify({"error": "MongoDB not connected"}), 500
    
    try:
        city = request.args.get('city')
        limit = int(request.args.get('limit', 100))
        
        query = {}
        if city:
            query['city'] = city
        
        # Get data sorted by timestamp (newest first)
        cursor = aqi_collection.find(query).sort('timestamp', -1).limit(limit)
        
        data = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
            data.append(doc)
        
        return jsonify({
            "success": True,
            "count": len(data),
            "data": data
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/export-to-csv', methods=['POST'])
def export_to_csv():
    """Export MongoDB data to CSV dataset"""
    if aqi_collection is None:
        return jsonify({"error": "MongoDB not connected"}), 500
    
    try:
        # Get all data from MongoDB
        cursor = aqi_collection.find({})
        
        new_rows = []
        for doc in cursor:
            new_row = {
                'CO': doc['pollutants']['CO'],
                'NO2': doc['pollutants']['NO2'],
                'PM2.5': doc['pollutants']['PM2.5'],
                'SO2': doc['pollutants']['SO2'],
                'AQI': doc['prediction']['aqi'],
                'health_impact': doc['prediction']['health_impact'],
                'Precautionary_Measures': doc['prediction']['precautionary_measures'],
                'city': doc['city'],
                'timestamp': doc['timestamp']
            }
            new_rows.append(new_row)
        
        if new_rows:
            # Load existing dataset
            try:
                existing_df = pd.read_csv(DATA_FILE)
            except:
                existing_df = pd.DataFrame()
            
            # Create DataFrame from MongoDB data
            new_df = pd.DataFrame(new_rows)
            
            # Append new data to existing dataset
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            
            # Remove duplicates if any
            combined_df = combined_df.drop_duplicates()
            
            # Save back to CSV
            combined_df.to_csv(DATA_FILE, index=False)
            
            return jsonify({
                "success": True,
                "message": f"Exported {len(new_rows)} records to dataset",
                "file": DATA_FILE
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "No data to export"
            }), 200
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/mongodb-stats', methods=['GET'])
def mongodb_stats():
    """Get MongoDB collection statistics"""
    if aqi_collection is None:
        return jsonify({"connected": False, "error": "MongoDB not connected"}), 500
    
    try:
        total_count = aqi_collection.count_documents({})
        
        # Get unique cities
        cities = aqi_collection.distinct('city')
        
        # Get latest record
        latest = aqi_collection.find_one(sort=[('timestamp', -1)])
        
        return jsonify({
            "connected": True,
            "total_records": total_count,
            "unique_cities": len(cities),
            "cities": cities,
            "latest_timestamp": latest['timestamp'] if latest else None
        }), 200
        
    except Exception as e:
        return jsonify({"connected": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)


