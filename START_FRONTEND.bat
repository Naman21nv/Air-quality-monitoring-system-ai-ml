@echo off
echo ========================================
echo   Starting Frontend (Vite Dev Server)
echo ========================================
echo.
cd /d "%~dp0frontend"
echo Current directory: %CD%
echo.
echo Starting Vite dev server...
echo Frontend will be available at http://localhost:5173
echo Press Ctrl+C to stop the server
echo.
npm run dev
pause
