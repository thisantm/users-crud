#!/bin/bash

# Navigate to the server directory
cd server

# Check if the Python environment exists
if [ -d "venv" ]; then
    echo "Python environment exists, skipping creation"
    # Activate the environment
    source ./venv/bin/activate
else
    # Create a Python environment
    python3 -m venv venv
    # Activate the environment
    source ./venv/bin/activate
    # Install the necessary Python packages
    pip install -r requirements.txt
fi

# Run the server
flask --app server.py run
