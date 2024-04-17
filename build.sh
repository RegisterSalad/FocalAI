#!/bin/bash

# Define paths and environment variables
ANACONDA_PATH="$HOME/anaconda3"
ENV_NAME="FocalAI"
PYTHON_VERSION="3.12.1"
LOG_FILE="build_log.log"
APP_PATH="./app"

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

# Check and manage the Anaconda environment based on the -clean flag
if [[ "$1" == "-clean" ]]; then
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
elif ! conda info --envs | grep $ENV_NAME; then
    echo "Environment $ENV_NAME does not exist. Creating new one..." | tee -a $LOG_FILE
    conda create --name $ENV_NAME python=$PYTHON_VERSION -y >> $LOG_FILE 2>&1
fi

# Activate the Anaconda environment
echo "Activating the Anaconda environment..." | tee -a $LOG_FILE
conda activate $ENV_NAME

# Check for pip and PyInstaller installation
pip freeze | grep -q 'pyinstaller'
if [ $? -ne 0 ]; then
    echo "Installing PyInstaller..." | tee -a $LOG_FILE
    pip install pyinstaller >> $LOG_FILE 2>&1
fi
pip freeze | grep -q 'pip$'
if [ $? -ne 0 ]; then
    echo "Upgrading pip..." | tee -a $LOG_FILE
    pip install --upgrade pip >> $LOG_FILE 2>&1
fi

# Install other dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..." | tee -a $LOG_FILE
pip install -r requirements.txt >> $LOG_FILE 2>&1

# Clean previous builds if -clean is specified
if [[ "$1" == "-clean" ]]; then
    echo "Cleaning previous builds..." | tee -a $LOG_FILE
    rm -rf build/ $APP_PATH/ >> $LOG_FILE 2>&1
fi

echo "Building the application with FocalAI.py and additional paths..." | tee -a $LOG_FILE
pyinstaller src/frontend_build/FocalAI.py --noconfirm --clean --onefile --windowed \
  --paths=./src/frontend_build/ \
  --paths=./src/ \
  --distpath $APP_PATH >> $LOG_FILE 2>&1  # Make sure there's no space after the backslash on the previous line
if [ $? -ne 0 ]; then
    echo "PyInstaller failed to build the application, exiting with status 1" | tee -a $LOG_FILE
    exit 1
fi
echo "Build completed. Check the '$APP_PATH' directory for the executable." | tee -a $LOG_FILE
echo "Executable path: $(pwd)$APP_PATH/FocalAI" | tee -a $LOG_FILE  # Corrected to properly display the full path
echo "Install Log File: $LOG_FILE" | tee -a $LOG_FILE
