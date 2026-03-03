#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Start Flask app in a new Terminal window
osascript -e "tell application \"Terminal\" to do script \"cd '$SCRIPT_DIR/Assets' && python3 App.py\""

# Start ngrok in a new Terminal window
osascript -e "tell application \"Terminal\" to do script \"cd '$SCRIPT_DIR/Assets/ngrok-v3-stable-darwin-amd64' && ./ngrok http 8090\""

# Start Test.py (Signal sender) in a new Terminal window
osascript -e "tell application \"Terminal\" to do script \"cd '$SCRIPT_DIR/Assets' && python3 Test.py\""