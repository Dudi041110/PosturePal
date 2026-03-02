@echo off

REM Start Flask app in a new terminal
start "" cmd /k "cd /d Assets && python App.py"

REM Start ngrok in a new terminal
start "" cmd /k "cd /d Assets\ngrok-v3-stable-windows-amd64 && ngrok http 8090"

REM Start Test.py (Signal sender) in a new terminal
start "" cmd /k "cd /d Assets && python Test.py"

pause