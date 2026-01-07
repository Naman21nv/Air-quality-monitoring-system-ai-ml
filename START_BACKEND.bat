@echo off
echo ========================================
echo   Starting Backend Server (Flask + MongoDB)
echo ========================================
echo.
cd /d "%~dp0backend"
echo Current directory: %CD%
echo.
echo Starting Flask backend on http://127.0.0.1:5000
echo MongoDB Atlas will connect automatically
echo Press Ctrl+C to stop the server
echo.
python app.py
pause
