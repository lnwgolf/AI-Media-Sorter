@echo off
title AI Media Sorter Launcher
cd /d "%~dp0"

echo ========================================================
echo        AI Media Sorter - Quick Launcher (Windows)
echo ========================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please download and install Python 3.10+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Create Virtual Environment if not exists
if not exist "venv" (
    echo [INFO] Creating Python virtual environment (venv)...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: Activate Virtual Environment
call venv\Scripts\activate.bat

:: Install / verify dependencies
echo [INFO] Checking and installing dependencies...
pip install -r requirements.txt --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo [WARNING] Some dependencies might have failed to install. Trying to run anyway...
)

echo.
echo [INFO] Starting AI Media Sorter...
echo.
python AI_Image_Sorter.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application closed with an error.
    pause
)
