# ⚠️ API TOKEN ISSUE DETECTED

## Problem
Your WAQI (World Air Quality Index) API token is **invalid** or **expired**.

## Error Message You're Seeing
"City not found or API limit exceeded"

## Actual Problem
The API token in your code is invalid: `175620:698a982d-11c2-40cf-ad1e-b5a2fc4a29c2`

## ✅ Solution - Get a New API Token

### Step 1: Get a Free Token
1. Visit: **https://aqicn.org/data-platform/token/**
2. Fill in your details (name, email, organization)
3. You'll receive a token via email (looks like: `abc123def456...`)

### Step 2: Update Your Code

Update the token in **TWO files**:

#### File 1: `frontend/src/App.jsx`
Find line ~8:
```javascript
const TOKEN = "175620:698a982d-11c2-40cf-ad1e-b5a2fc4a29c2";
```

Replace with your new token:
```javascript
const TOKEN = "YOUR_NEW_TOKEN_HERE";
```

#### File 2: `air/App.jsx` (if you're using this one)
Same change - find and replace the TOKEN constant.

### Step 3: Restart Frontend
```powershell
# Stop the frontend (Ctrl+C)
# Then restart:
cd d:\air\air\frontend
npm run dev
```

### Step 4: Test
1. Open the app in browser
2. Search for "Delhi" or "Mumbai"
3. Should now work!

---

## 🔄 Alternative: Test with Demo Cities

If you don't want to get a new token, you can modify the app to use demo/static data for testing.

---

## 🧪 Test Your New Token

After getting a new token, test it:
```powershell
cd d:\air\air\backend
# Edit test_waqi_api.py and replace TOKEN
python test_waqi_api.py
```

Should see ✅ SUCCESS for all cities!

---

## 📝 Current Status
- ✅ Backend is working correctly
- ✅ Frontend is working correctly  
- ✅ Connection between frontend/backend is fixed
- ❌ **WAQI API token is invalid** ← You are here

Once you update the token, everything will work!
