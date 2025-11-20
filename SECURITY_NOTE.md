# 🔐 Security Notice

## API Token Configuration

⚠️ **IMPORTANT:** Never commit your real API token to GitHub!

### How to Use Your Token Securely:

1. **Frontend:** Create a `.env` file in the `frontend/` folder:
   ```
   VITE_WAQI_TOKEN=your_actual_token_here
   VITE_BACKEND_URL=http://localhost:5000
   ```

2. **Backend:** Set environment variable:
   ```powershell
   $env:WAQI_TOKEN="your_actual_token_here"
   ```

3. **Never commit `.env` files** - they are already in `.gitignore`

### Current Setup:
- ✅ `.env` files are in `.gitignore`
- ✅ Code uses environment variables
- ✅ Demo token is used as fallback for testing

### If Your Token Was Exposed:
1. Get a new token from https://aqicn.org/data-platform/token/
2. Update your `.env` files
3. Never push `.env` to GitHub
