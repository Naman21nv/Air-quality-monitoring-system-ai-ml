import pandas as pd
import numpy as np
import os
import joblib
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv1D, LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical

# =======================
# CONFIGURATION
# =======================
DATA_FILE = r"D:\air\air\backend\corrected_precautionary_data.csv"
MODEL_FILE = "pollution_cnn_lstm_model.h5"
SCALER_FILE = "pollution_scaler.pkl"
LABEL_ENCODER_FILE = "pollution_label_encoder.pkl"

features = ["CO", "NO2", "PM2.5", "SO2"]

# =======================
# TRAIN MODEL IF NOT EXISTS
# =======================
if not os.path.exists(MODEL_FILE):
    print("⚡ Training model for the first time...")

    df = pd.read_csv(DATA_FILE)
    X = df[features].values

    # Encode source labels
    label_encoder = LabelEncoder()
    df["source_encoded"] = label_encoder.fit_transform(df["source_label"])
    y = df["source_encoded"].values

    # Scale features
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = X_scaled.reshape((X_scaled.shape[0], X_scaled.shape[1], 1))  # (samples, 4, 1)

    # CNN + LSTM model
    model = Sequential([
        Conv1D(64, kernel_size=2, activation='relu', input_shape=(X_scaled.shape[1], 1)),
        LSTM(50, return_sequences=False),
        Dropout(0.3),
        Dense(len(np.unique(y)), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_scaled, to_categorical(y), epochs=10, batch_size=4, verbose=1)

    # Save model + preprocessors
    model.save(MODEL_FILE)
    joblib.dump(scaler, SCALER_FILE)
    joblib.dump(label_encoder, LABEL_ENCODER_FILE)

    print("✅ Model and preprocessors saved successfully.")
else:
    print("✅ Model already trained. Skipping training.")

# =======================
# LOAD MODEL & DATA
# =======================
model = load_model(MODEL_FILE)
scaler = joblib.load(SCALER_FILE)
label_encoder = joblib.load(LABEL_ENCODER_FILE)
df = pd.read_csv(DATA_FILE)

# =======================
# USER INPUT LOOP
# =======================
while True:
    print("\nEnter pollutant values (or type 'exit' to quit):")
    co = input("CO: ")
    if co.lower() == "exit": break
    no2 = input("NO2: ")
    if no2.lower() == "exit": break
    pm25 = input("PM2.5: ")
    if pm25.lower() == "exit": break
    so2 = input("SO2: ")
    if so2.lower() == "exit": break

    try:
        co, no2, pm25, so2 = float(co), float(no2), float(pm25), float(so2)
    except ValueError:
        print("❌ Invalid input. Please enter numeric values.")
        continue

    # Scale input
    user_input = np.array([[co, no2, pm25, so2]])
    user_scaled = scaler.transform(user_input)
    user_scaled = user_scaled.reshape((1, 4, 1))   # ✅ FIXED reshape

    # Predict
    pred_source_idx = np.argmax(model.predict(user_scaled), axis=1)[0]
    pred_source = label_encoder.inverse_transform([pred_source_idx])[0]

    # Match closest row for extra info
    try:
        closest_row = df.iloc[((df[features] - user_input) ** 2).sum(axis=1).idxmin()]
        pred_health = closest_row.get("health_impact", "N/A")
        pred_measures = closest_row.get("Precautionary_Measures", "N/A")
        pred_aqi = closest_row.get("AQI", "N/A")
    except Exception as e:
        pred_health, pred_measures, pred_aqi = "N/A", "N/A", "N/A"

    # Display results
    print("\n--- Prediction ---")
    print(f"Source Label: {pred_source}")
    print(f"Health Impact: {pred_health}")
    print(f"Precautionary Measures: {pred_measures}")
    print(f"AQI: {pred_aqi}")

print("\n👋 Exiting Continuous Prediction Mode.")
