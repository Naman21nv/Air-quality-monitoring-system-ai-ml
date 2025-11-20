# QUICK START - Air Quality Monitor

## 🚀 Start Your Application in 3 Steps:

### Step 1: Start Backend
Open PowerShell/Terminal and run:
```powershell
cd d:\air\air\backend
python app.py
```
**Wait for:** `* Running on http://0.0.0.0:5000`

### Step 2: Start Frontend  
Open a NEW PowerShell/Terminal and run:
```powershell
cd d:\air\air\frontend
npm run dev
```
**Wait for:** `Local: http://localhost:5173/`

### Step 3: Open Browser
Go to: http://localhost:5173

---

## ✅ Quick Test:
1. Type "Delhi" in the search box
2. Click "Check"
3. Open browser console (F12) to see connection logs
4. You should see AQI data and charts!

---

## 🔧 If It Doesn't Work:

### Backend Issues:
- **Error: "No module named flask"**
  ```powershell
  cd d:\air\air\backend
  pip install -r requirements.txt
  ```

- **Error: "Port 5000 already in use"**
  - Stop other programs using port 5000
  - Or change port in both `backend/app.py` and `frontend/src/App.jsx`

### Frontend Issues:
- **Error: "Cannot find module"**
  ```powershell
  cd d:\air\air\frontend
  npm install
  ```

- **Error: "Cannot connect to backend"**
  - Make sure backend is running first!
  - Check http://localhost:5000 shows API message

---

## 📝 What's Fixed:
✅ Backend URL changed from 127.0.0.1 to localhost  
✅ CORS properly configured  
✅ Better error messages in console  
✅ Improved connection handling  

---

## 🆘 Still Having Issues?
1. Check `CONNECTION_FIX_GUIDE.md` for detailed troubleshooting
2. Run `python test_backend.py` to test backend
3. Check browser console (F12) for error messages
