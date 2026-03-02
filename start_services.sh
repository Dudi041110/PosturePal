#!/bin/bash

# Start Flask app in a new Terminal window
osascript -e 'tell application "Terminal" to do script "cd ~/path/to/Assets && python3 App.py"'

# Start ngrok in a new Terminal window
osascript -e 'tell application "Terminal" to do script "cd ~/path/to/Assets/ngrok-v3-stable-darwin-amd64 && ./ngrok http 8090"'

# Start Test.py (Signal sender) in a new Terminal window
osascript -e 'tell application "Terminal" to do script "cd ~/path/to/Assets && python3 Test.py"'