@echo off
echo ========================================
echo   Air Quality Monitoring System
echo ========================================
echo.
echo This will start BOTH backend and frontend
echo.
echo Backend: http://127.0.0.1:5000
echo Frontend: http://localhost:5173
echo MongoDB Viewer: view_mongodb_data.html
echo.
echo Press any key to start both servers...
pause >nul

echo.
echo Starting Backend in new window...
start "Backend Server" cmd /k "%~dp0START_BACKEND.bat"

echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak >nul

echo Starting Frontend in new window...
start "Frontend Server" cmd /k "%~dp0START_FRONTEND.bat"

echo.
echo ========================================
echo   SERVERS STARTED!
echo ========================================
echo.
echo Backend running at: http://127.0.0.1:5000
echo Frontend running at: http://localhost:5173
echo.
echo To view MongoDB data, open: view_mongodb_data.html
echo.
echo Close the server windows to stop the application.
echo.
pause
