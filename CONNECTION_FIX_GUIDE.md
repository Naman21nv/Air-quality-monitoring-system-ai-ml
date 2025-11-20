# Air Quality Monitor - Connection Fix Guide

## Problem Identified
Your frontend and backend work separately but don't communicate. Here's what was fixed:

### Issues Found:
1. **Backend URL mismatch**: Frontend was using `127.0.0.1` instead of `localhost`
2. **CORS headers**: Backend CORS needed proper configuration
3. **Missing error handling**: Frontend wasn't showing clear connection errors

## What Was Changed:

### 1. Frontend (App.jsx)
- ✅ Changed backend URL from `http://127.0.0.1:5000` to `http://localhost:5000`
- ✅ Added detailed error logging to console
- ✅ Added proper headers to API requests
- ✅ Improved error messages to users

### 2. Backend (app.py)
- ✅ Improved CORS configuration
- ✅ Added proper headers for cross-origin requests
- ✅ Backend already has all necessary endpoints

## How to Run Your Application:

### Option 1: Using Batch Files (Easiest)
1. Open TWO separate terminals/command prompts
2. Terminal 1: Double-click `START_BACKEND.bat` or run:
   ```
   cd d:\air\air
   START_BACKEND.bat
   ```
3. Terminal 2: Double-click `START_FRONTEND.bat` or run:
   ```
   cd d:\air\air
   START_FRONTEND.bat
   ```

### Option 2: Manual Start

#### Terminal 1 - Backend:
```powershell
cd d:\air\air\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Wait for: `* Running on http://0.0.0.0:5000`

#### Terminal 2 - Frontend:
```powershell
cd d:\air\air\frontend
npm install
npm run dev
```

Wait for: `Local: http://localhost:5173/` (or similar)

### Option 3: Test Backend First
Before starting frontend, verify backend works:
```powershell
cd d:\air\air\backend
.\venv\Scripts\Activate.ps1
python test_backend.py
```

This will test if:
- Backend server is running
- Predict endpoint is working
- Model files are loaded correctly

## Troubleshooting:

### If frontend can't connect to backend:

1. **Check backend is running**
   - Look for: `* Running on http://0.0.0.0:5000`
   - Test: Open http://localhost:5000 in browser
   - Should see: `{"message": "Air Quality Monitoring API is running"}`

2. **Check for port conflicts**
   - Make sure nothing else is using port 5000
   - Check with: `netstat -ano | findstr :5000`

3. **Check browser console**
   - Open browser DevTools (F12)
   - Go to Console tab
   - Look for errors when searching for a city
   - Check Network tab for failed requests

4. **Common errors and fixes:**

   **Error: "Cannot connect to backend"**
   - Backend not running → Start backend first
   - Wrong port → Check backend says port 5000
   
   **Error: "CORS policy"**
   - Already fixed in code
   - Restart backend if it was already running
   
   **Error: "Model not loaded"**
   - Check these files exist in `backend/`:
     - pollution_cnn_lstm_model.h5
     - pollution_scaler.pkl
     - pollution_label_encoder.pkl
     - corrected_precautionary_data.csv

## Testing the Connection:

1. Start backend (Terminal 1)
2. Start frontend (Terminal 2)
3. Open http://localhost:5173 (or the port Vite shows)
4. Open browser DevTools (F12) → Console tab
5. Search for "Delhi" or another city
6. Check console for:
   - "Sending to backend: {...}" → Frontend sending request ✅
   - "Backend response: {...}" → Backend responding ✅
   - If you see errors → Copy them and check the error message

## Expected Console Output:

When working correctly, you should see:
```
Sending to backend: {CO: 2.5, NO2: 45, PM2.5: 55, SO2: 12, city_name: "Delhi"}
Backend response: {source: "...", health_impact: "...", precautionary_measures: "...", aqi: 150}
```

## Port Numbers:
- **Backend (Flask)**: http://localhost:5000
- **Frontend (Vite)**: http://localhost:5173 (usually, may vary)

## Files Modified:
- ✅ `frontend/src/App.jsx` - Fixed API calls
- ✅ `App.jsx` (root) - Fixed API calls
- ✅ `backend/app.py` - Improved CORS
- ✅ Created helper scripts for easy startup

## Next Steps:
1. Close any running terminals
2. Start fresh using the batch files or manual steps above
3. Test with "Delhi" first (has good data)
4. Check browser console for any errors
5. If issues persist, run `test_backend.py` to diagnose

Need more help? Check the error messages in the console!
