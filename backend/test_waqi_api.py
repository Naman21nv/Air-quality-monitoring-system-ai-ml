import requests
import json

# Test the WAQI API token
import os
TOKEN = os.getenv("WAQI_TOKEN", "demo")  # Get from environment or use demo
test_cities = ["Delhi", "Mumbai", "London", "New York"]

print("=" * 60)
print("TESTING WAQI API TOKEN")
print("=" * 60)
print(f"Token: {TOKEN}")
print()

for city in test_cities:
    print(f"Testing city: {city}")
    print("-" * 40)
    
    try:
        url = f"https://api.waqi.info/feed/{city}/?token={TOKEN}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"API Status: {data.get('status')}")
        
        if data.get('status') == 'ok':
            print(f"✅ SUCCESS - City: {city}")
            aqi_data = data.get('data', {})
            aqi = aqi_data.get('aqi', 'N/A')
            print(f"   AQI: {aqi}")
            
            # Check pollutants
            iaqi = aqi_data.get('iaqi', {})
            print(f"   Pollutants available:")
            for pollutant in ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3']:
                value = iaqi.get(pollutant, {}).get('v', 'N/A')
                if value != 'N/A':
                    print(f"      - {pollutant.upper()}: {value}")
        else:
            print(f"❌ FAILED - {data.get('data', 'Unknown error')}")
            
    except requests.exceptions.Timeout:
        print(f"❌ TIMEOUT - Request took too long")
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION ERROR - Check internet connection")
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")
    
    print()

print("=" * 60)
print("\nNOTES:")
print("- If all tests failed with 'Invalid key', your API token is invalid")
print("- Get a new token at: https://aqicn.org/data-platform/token/")
print("- Update the TOKEN constant in frontend/src/App.jsx")
print("=" * 60)
