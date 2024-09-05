#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install it before proceeding."
    exit 1
fi

# Create a virtual environment in a directory named 'venv' if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Load AWS credentials from aws_credentials.txt and export them within the virtual environment
if [ -f aws_credentials.txt ]; then
    echo "Loading AWS credentials into the virtual environment..."
    export $(grep -v '^#' aws_credentials.txt | xargs)
else
    echo "aws_credentials.txt file not found!"
    deactivate
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f requirements.txt ]; then
    echo "requirements.txt not found!"
    deactivate
    exit 1
fi

# Install the required Python packages
echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Run the Python script bedrock.py
if [ ! -f bedrock.py ]; then
    echo "bedrock.py not found!"
    deactivate
    exit 1
fi

echo "Running bedrock.py..."
python bedrock.py

# Deactivate the virtual environment after execution
echo "Deactivating virtual environment..."
deactivate
