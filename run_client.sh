#!/bin/bash

# Navigate to the client directory
cd client

# Check if node_modules exists
if [ -d "node_modules" ]; then
    echo "node_modules exists, skipping npm install"
else
    # Install the necessary npm packages
    npm install
fi

# Run the client
npm run dev
