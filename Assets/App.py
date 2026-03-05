from flask import Flask, request, jsonify, render_template
from pywebpush import webpush, WebPushException
import json
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

app = Flask(__name__, template_folder=resource_path("templates"))

subscriptions = []

# Sensitivity threshold (mirrors xThreshold in the .ino)
# Default matches the Arduino's original hardcoded value
sensitivity = 1000

VAPID_PUBLIC_KEY = "BE7yy_U1yIwrZzcy_DuirX8HqfNjLqZH8qi4ZNdjyz0nb1Go99jlMfm55bZlYQKLDCLrz0mxuWeft6NFofcU24U="
VAPID_PRIVATE_KEY = "MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgw69nwGQXVxxRsXGkGqTTx12uRRUbIYE_RabSWwvhmIuhRANCAARO8sv1NciMK2c3Mvw7oq1_B6nzYy6mR_KouGTXY8s9J29RqPfY5TH5ueW2ZWECiwwi689Jsblnn7ejRaH3FNuF"

@app.route("/")
def index():
    return render_template("index.html")

# Phone registers here
@app.route("/subscribe", methods=["POST"])
def subscribe():
    sub = request.json
    if sub not in subscriptions:
        subscriptions.append(sub)
    return {"status": "subscribed"}

# ESP triggers this
@app.route("/signal")
def signal():
    for sub in subscriptions[:]:
        try:
            webpush(
                subscription_info=sub,
                data=json.dumps({
                    "title": "Posture Alert",
                    "body": "Bad posture detected!"
                }),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims={"sub": "mailto:test@test.com"}
            )
        except WebPushException as ex:
            if ex.response and ex.response.status_code == 410:
                print("Removing expired subscription")
                subscriptions.remove(sub)
            else:
                raise
    return "Push sent"

@app.route("/vapidPublicKey")
def vapid_key():
    return VAPID_PUBLIC_KEY

# --- Sensitivity endpoints ---

@app.route("/setSensitivity", methods=["POST"])
def set_sensitivity():
    """Called by the web app slider to update the threshold."""
    global sensitivity
    data = request.json
    if data is None or "value" not in data:
        return jsonify({"error": "Missing 'value' field"}), 400
    val = int(data["value"])
    # Clamp to a sane range (100 = very sensitive, 5000 = very lenient)
    sensitivity = max(100, min(5000, val))
    print(f"Sensitivity updated to: {sensitivity}")
    return jsonify({"status": "ok", "sensitivity": sensitivity})

@app.route("/getSensitivity")
def get_sensitivity():
    """Polled by the Arduino every few seconds to read the current threshold."""
    return jsonify({"sensitivity": sensitivity})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)