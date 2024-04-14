#!/bin/bash

# Define the path to the virtual environment and Python version
VENV_DIR="./venv"
PYTHON_VERSION="3.12.1"

# Delete the existing virtual environment to ensure a clean slate
echo "Deleting existing virtual environment..."
rm -rf $VENV_DIR

# Create a new virtual environment with the specific Python version
echo "Creating new virtual environment with Python $PYTHON_VERSION..."
pyenv local $PYTHON_VERSION
python -m venv $VENV_DIR

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Upgrade pip and ensure PyInstaller is installed
echo "Installing/updating pip and PyInstaller..."
pip install --upgrade pip
pip install pyinstaller

# Install other dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r pip_reqs/requirements.txt

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/

# Build the PyQt application
echo "Building the application..."
pyinstaller --noconfirm --log-level=INFO \
            --paths=./src/ \
            --additional-hooks-dir=./hooks/ \
            --onefile \
            --windowed \
            --name=FocalAI \
            --add-data "src/frontend_build;frontend_build" \
            src/frontend_build/mainwindow.py

echo "Build completed. Check the 'dist/' directory for the executable."
