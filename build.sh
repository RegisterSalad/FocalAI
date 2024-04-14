#!/bin/bash

# Define paths and environment variables
ANACONDA_PATH="$HOME/anaconda3"
ENV_NAME="FocalAI"
PYTHON_VERSION="3.12.1"
LOG_FILE="./build_log.txt"

# Start new log file
echo "Starting build process..." > $LOG_FILE

# Initialize Conda for script usage
echo "Initializing Conda..."
source "$ANACONDA_PATH/etc/profile.d/conda.sh"

# Check if Conda was sourced correctly
if [ $? -ne 0 ]; then
    echo "Failed to source Conda, exiting..." | tee -a $LOG_FILE
    exit 1
fi

# Activate the Anaconda environment, if it exists
echo "Checking if environment $ENV_NAME exists..."
if conda info --envs | grep $ENV_NAME; then
    echo "Deleting existing Anaconda environment..." | tee -a $LOG_FILE
    conda remove --name $ENV_NAME --all -y >> $LOG_FILE 2>&1
    if [ $? -ne 0 ]; then
        echo "Failed to remove existing environment, exiting..." | tee -a $LOG_FILE
        exit 1
    fi
fi

echo "Creating new Anaconda environment with Python $PYTHON_VERSION..." | tee -a $LOG_FILE
conda create --name $ENV_NAME python=$PYTHON_VERSION -y >> $LOG_FILE 2>&1
if [ $? -ne 0 ]; then
    echo "Failed to create new environment, exiting..." | tee -a $LOG_FILE
    exit 1
fi

# Reactivate to ensure changes take effect
echo "Activating the Anaconda environment..." | tee -a $LOG_FILE
conda activate $ENV_NAME
if [ $? -ne 0 ]; then
    echo "Failed to activate environment, exiting..." | tee -a $LOG_FILE
    exit 1
fi

# Upgrade pip and ensure PyInstaller is installed
echo "Installing/updating pip and PyInstaller..." | tee -a $LOG_FILE
pip install --upgrade pip >> $LOG_FILE 2>&1
pip install pyinstaller >> $LOG_FILE 2>&1
if [ $? -ne 0 ]; then
    echo "Failed to install required packages, exiting..." | tee -a $LOG_FILE
    exit 1
fi

# Install other dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..." | tee -a $LOG_FILE
pip install -r pip_reqs/requirements.txt >> $LOG_FILE 2>&1
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies, exiting..." | tee -a $LOG_FILE
    exit 1
fi

# Clean previous builds
echo "Cleaning previous builds..." | tee -a $LOG_FILE
rm -rf build/ dist/ >> $LOG_FILE 2>&1

echo "Building the application with FocalAI.py and additional paths..." | tee -a $LOG_FILE
pyinstaller src/frontend_build/FocalAI.py --noconfirm --clean --onefile --windowed \
  --paths=./src/frontend_build/ \
  --paths=./src/ \
  >> $LOG_FILE 2>&1
if [ $? -ne 0 ]; then
    echo "PyInstaller failed to build the application, exiting with status 1" | tee -a $LOG_FILE
    exit 1
fi
echo "Build completed. Check the 'dist/' directory for the executable." | tee -a $LOG_FILE
echo "Executable path: $(pwd)/dist/" | tee -a $LOG_FILE
echo "Install Log File: $LOG_FILE" | tee -a $LOG_FILE
