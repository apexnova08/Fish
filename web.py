from flask import Flask, request
import requests, base64
from threading import Thread
import json
import os

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
CLIENT_ID = "19c85a65b9b948d784d6bd75f6ef3c55"
SECRET = "eat_XUc72EppAuYEyAMk5uHybsEcbgi7dslo_2rHJTj"

@app.route('/callback')
def callback():
    code = request.args.get("code")
    discord_id = request.args.get("state")

    auth = base64.b64encode(f"{CLIENT_ID}:{SECRET}".encode()).decode()

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

    tokendict = {discord_id: tokens}
    with open(dir + "\\tokens.json", "w") as f: json.dump(tokendict, f, indent=4)

    return "Login successful. You can close this."

# -------------------
# RUN SERVER IN THREAD
# -------------------
def run():
    app.run(host="0.0.0.0", port=5000)

def keep_alive():
    t = Thread(target=run)
    t.start()