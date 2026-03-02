from flask import Flask, request, jsonify, render_template
from pywebpush import webpush
import json

app = Flask(__name__)

subscriptions = []

VAPID_PUBLIC_KEY = "BE7yy_U1yIwrZzcy_DuirX8HqfNjLqZH8qi4ZNdjyz0nb1Go99jlMfm55bZlYQKLDCLrz0mxuWeft6NFofcU24U="
VAPID_PRIVATE_KEY = "MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgw69nwGQXVxxRsXGkGqTTx12uRRUbIYE_RabSWwvhmIuhRANCAARO8sv1NciMK2c3Mvw7oq1_B6nzYy6mR_KouGTXY8s9J29RqPfY5TH5ueW2ZWECiwwi689Jsblnn7ejRaH3FNuF"

@app.route("/")
def index():
    return render_template("index.html")


# phone registers here
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

    for sub in subscriptions:
        webpush(
            subscription_info=sub,
            data=json.dumps({
                "title": "Posture Alert",
                "body": "Bad posture detected!"
            }),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": "mailto:test@test.com"}
        )

    return "Push sent"


@app.route("/vapidPublicKey")
def vapid_key():
    return VAPID_PUBLIC_KEY


app.run(host="0.0.0.0", port=8090)