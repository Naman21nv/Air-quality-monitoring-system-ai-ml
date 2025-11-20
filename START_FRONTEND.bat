@echo off
echo Starting Frontend (Vite Dev Server)...
echo.
cd /d "%~dp0frontend"
echo Current directory: %CD%
echo.
echo Installing dependencies if needed...
if not exist node_modules (
    echo Installing npm packages...
    npm install
)
echo.
echo Starting Vite dev server...
npm run dev
pause
