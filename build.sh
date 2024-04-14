#!/bin/bash

# Define the Anaconda environment name, Python version, and log file path
ENV_NAME="FocalAI"
PYTHON_VERSION="3.12.1"
LOG_FILE="./build_log.txt"

# Start new log file
echo "Starting build process..." > $LOG_FILE

# Delete the existing Anaconda environment to ensure a clean slate
echo "Deleting existing Anaconda environment..." | tee -a $LOG_FILE
conda remove --name $ENV_NAME --all -y >> $LOG_FILE 2>&1

# Create a new Anaconda environment with the specific Python version
echo "Creating new Anaconda environment with Python $PYTHON_VERSION..." | tee -a $LOG_FILE
conda create --name $ENV_NAME python=$PYTHON_VERSION -y >> $LOG_FILE 2>&1

# Initialize Conda for script usage
echo "Initializing Conda..."
source ~/anaconda3/etc/profile.d/conda.sh

# Activate the Anaconda environment
echo "Activating the Anaconda environment..." | tee -a $LOG_FILE
conda activate $ENV_NAME

# Upgrade pip and ensure PyInstaller is installed
echo "Installing/updating pip and PyInstaller..." | tee -a $LOG_FILE
pip install --upgrade pip >> $LOG_FILE 2>&1
pip install pyinstaller >> $LOG_FILE 2>&1

# Install other dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..." | tee -a $LOG_FILE
pip install -r pip_reqs/requirements.txt >> $LOG_FILE 2>&1

# Clean previous builds
echo "Cleaning previous builds..." | tee -a $LOG_FILE
rm -rf build/ dist/ >> $LOG_FILE 2>&1

# Build the PyQt application
echo "Building the application..." | tee -a $LOG_FILE
pyinstaller --noconfirm --log-level=INFO \
            --paths=./src/ \
            --additional-hooks-dir=./hooks/ \
            --onefile \
            --windowed \
            --name=FocalAI \
            --add-data "src/frontend_build:frontend_build" \
            src/frontend_build/mainwindow.py >> $LOG_FILE 2>&1

echo "Build completed. Check the 'dist/' directory for the executable." | tee -a $LOG_FILE
echo "Executable path: $(pwd)/dist/" | tee -a $LOG_FILE
echo "Install Log File: $LOG_FILE" | tee -a $LOG_FILE