#!/bin/bash

# Start the Flask backend server
echo "Starting Flask backend on port 5050..."
cd "$(dirname "$0")"
python3 app.py
