import requests
import json

# Test if backend is running
backend_url = "http://localhost:5000"

print("Testing backend connectivity...")
print(f"Backend URL: {backend_url}")
print("-" * 50)

# Test 1: Check if server is running
try:
    response = requests.get(f"{backend_url}/")
    print("✅ Backend is running!")
    print(f"Response: {response.json()}")
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to backend. Make sure Flask app is running.")
    print("Run: python app.py")
    exit(1)

print("-" * 50)

# Test 2: Test the predict endpoint
test_data = {
    "CO": 2.5,
    "NO2": 45.0,
    "PM2.5": 55.0,
    "SO2": 12.0,
    "city_name": "Delhi"
}

print("\nTesting /predict endpoint...")
print(f"Sending data: {json.dumps(test_data, indent=2)}")

try:
    response = requests.post(
        f"{backend_url}/predict",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        print("✅ Predict endpoint working!")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"❌ Error: Status code {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Error calling predict endpoint: {str(e)}")

print("-" * 50)
print("\nIf all tests passed, your backend is working correctly!")
print("Make sure your frontend is calling http://localhost:5000/predict")
