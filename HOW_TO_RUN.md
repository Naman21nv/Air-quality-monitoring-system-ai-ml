# 🌍 Air Quality Monitoring System

## Quick Start Guide

### 🚀 Running the Project

**Option 1: Start Everything (Recommended)**
- Double-click `START_PROJECT.bat`
- This starts both backend and frontend automatically

**Option 2: Start Separately**
1. Double-click `START_BACKEND.bat` (starts Flask + MongoDB)
2. Double-click `START_FRONTEND.bat` (starts React frontend)

### 📱 Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://127.0.0.1:5000
- **MongoDB Viewer**: Open `view_mongodb_data.html` in browser

### 🔧 What's Running

**Backend (Port 5000)**
- Flask server with ML predictions
- MongoDB Atlas connection
- Auto-saves data to MongoDB and CSV

**Frontend (Port 5173)**
- React + Vite dev server
- Search any city for real-time air quality
- Shows AQI, predictions, health recommendations

**MongoDB Atlas**
- Cloud database storing all queries
- Auto-syncs to local CSV dataset

### 📊 View Your Data

1. Search for cities in the frontend
2. Open `view_mongodb_data.html` to see all stored data
3. Check `backend/corrected_precautionary_data.csv` for dataset

### 🔑 API Token

Your WAQI API token is already configured:
- Token: `81157ba943da574b26bb9c5be4b0af3f5a5182f1`
- Location: `frontend/.env` and `frontend/src/App.jsx`

### 🛑 Stopping the Project

- Close both terminal windows, OR
- Press Ctrl+C in each terminal window

### 📂 Project Structure

```
air/
├── START_PROJECT.bat         ← Start everything
├── START_BACKEND.bat         ← Start backend only
├── START_FRONTEND.bat        ← Start frontend only
├── view_mongodb_data.html    ← View MongoDB data
├── backend/
│   ├── app.py                ← Flask server
│   ├── corrected_precautionary_data.csv  ← Dataset
│   └── pollution_cnn_lstm_model.h5       ← ML model
└── frontend/
    ├── src/App.jsx           ← Main React app
    └── .env                  ← API token config
```

### 🔄 Data Flow

1. User searches city → Frontend
2. Frontend fetches WAQI API → Real pollution data
3. Backend ML prediction → AQI, health impact
4. **Auto-save to MongoDB Atlas** ✅
5. **Auto-save to CSV dataset** ✅
6. Display results to user

### 🗄️ MongoDB Atlas

- Database: `air_quality_db`
- Collection: `aqi_readings`
- Connection: Automatic on backend start
- View data: `view_mongodb_data.html`

### 🎯 Next Time You Run

Just double-click `START_PROJECT.bat` and everything will start automatically!
