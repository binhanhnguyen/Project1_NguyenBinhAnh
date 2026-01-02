@echo off
REM Quick launcher for Bách Khoa Pathfinding System
REM Double-click this file to run the app!

echo ========================================
echo  Bach Khoa Pathfinding System
echo  Local Setup and Launch
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [1/4] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Please ensure Python is installed and in PATH
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
    echo.
)

REM Activate virtual environment
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo.

REM Check if dependencies are installed
echo [3/4] Checking dependencies...
python -c "import streamlit" 2>nul
if errorlevel 1 goto install_deps
echo Dependencies already installed!
goto run_app

:install_deps
echo Installing dependencies (this may take 5-10 minutes)...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

:run_app

REM Run Streamlit app
echo [4/4] Starting Streamlit app...
echo.
echo ========================================
echo  App will open in your browser
echo  URL: http://localhost:8501
echo  Press Ctrl+C to stop the server
echo ========================================
echo.

streamlit run streamlit_run.py

REM If Streamlit exits, pause to show any errors
if errorlevel 1 (
    echo.
    echo ERROR: Streamlit failed to start
    pause
)

