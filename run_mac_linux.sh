#!/usr/bin/env bash
# AI Media Sorter - Quick Launcher for macOS & Linux

set -e
cd "$(dirname "$0")"

echo "========================================================"
echo "      AI Media Sorter - Quick Launcher (macOS/Linux)     "
echo "========================================================"
echo ""

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 is not installed or not in PATH."
    echo "Please install Python 3.10+ from https://www.python.org/ or via your package manager."
    exit 1
fi

# Create Virtual Environment if not exists
if [ ! -d "venv" ]; then
    echo "[INFO] Creating Python virtual environment (venv)..."
    python3 -m venv venv
fi

# Activate Virtual Environment
source venv/bin/activate

# Install / update dependencies
echo "[INFO] Checking and installing dependencies..."
pip install -r requirements.txt --quiet --disable-pip-version-check

echo ""
echo "[INFO] Starting AI Media Sorter..."
echo ""
python3 AI_Image_Sorter.py
