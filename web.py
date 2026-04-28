from flask import Flask, request
import requests, base64
from threading import Thread
import os
import eve
import funcsnfish as ff

app = Flask('')

dir = os.path.dirname(os.path.realpath(__file__))

# -------------------
# BASIC KEEP ALIVE ROUTE
# -------------------
@app.route('/')
def home():
    return "bot ok"

# -------------------
# EVE CALLBACK ROUTE
# -------------------

@app.route('/callback')
def callback():
    code = request.args.get("code")
    user = request.args.get("user")
    channel = request.args.get("channel")

    auth = base64.b64encode(f"{eve.CLIENT_ID}:{eve.SECRET}".encode()).decode()

    r = requests.post(
        "https://login.eveonline.com/v2/oauth/token",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "authorization_code",
            "code": code
        }
    )

    tokens = r.json()
    if channel != "none":
        tokens["channel"] = channel
        ff.updateProfile(user, tokens)

    return "Login successful. You can close this."

# -------------------
# RUN SERVER IN THREAD
# -------------------
def run():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()