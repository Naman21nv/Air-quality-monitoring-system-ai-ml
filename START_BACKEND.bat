@echo off
echo Starting Flask Backend...
echo.
cd /d "%~dp0backend"
echo Current directory: %CD%
echo.
echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo No virtual environment found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing requirements...
    pip install -r requirements.txt
)
echo.
echo Starting Flask app on port 5000...
python app.py
pause
