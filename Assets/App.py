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

VAPID_PUBLIC_KEY = "BE7yy_U1yIwrZzcy_DuirX8HqfNjLqZH8qi4ZNdjyz0nb1Go99jlMfm55bZlYQKLDCLrz0mxuWeft6NFofcU24U="
VAPID_PRIVATE_KEY = "MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgw69nwGQXVxxRsXGkGqTTx12uRRUbIYE_RabSWwvhmIuhRANCAARO8sv1NciMK2c3Mvw7oq1_B6nzYy6mR_KouGTXY8s9J29RqPfY5TH5ueW2ZWECiwwi689Jsblnn7ejRaH3FNuF"

@app.route("/")
def index():
    return render_template("index.html")

# Phone registers here
@app.route("/subscribe", methods=["POST"])
def subscribe():
    sub = request.json
    # Avoid duplicates
    if sub not in subscriptions:
        subscriptions.append(sub)
    return {"status": "subscribed"}

# ESP triggers this
@app.route("/signal")
def signal():
    for sub in subscriptions[:]:  # iterate over a copy to allow removal
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
            # Only remove if the subscription is truly gone
            if ex.response and ex.response.status_code == 410:
                print("Removing expired subscription")
                subscriptions.remove(sub)
            else:
                # If some other error, raise it
                raise
    return "Push sent"

@app.route("/vapidPublicKey")
def vapid_key():
    return VAPID_PUBLIC_KEY

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)