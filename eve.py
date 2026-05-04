import urllib.parse
import requests
import json
import os
import base64
import hotstuff as hs

from datetime import datetime, timezone

dir = os.path.dirname(os.path.realpath(__file__))

TOKEN_LINK = "https://login.eveonline.com/v2/oauth/token"
CLIENT_ID = "19c85a65b9b948d784d6bd75f6ef3c55"
SECRET = os.getenv("EVE_SECRET")
REDIRECT_URI = "https://fish-8v65.onrender.com/callback"
SCOPES = "esi-corporations.read_structures.v1"

def makeAuthUrl(userId, channel="none"):
    state = json.dumps({
        "user": str(userId),
        "channel": channel
    })

    return (
        "https://login.eveonline.com/v2/oauth/authorize?"
        + urllib.parse.urlencode({
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "scope": SCOPES,
            "state": state
        })
    )

def refreshToken(userId):
    p = hs.spGetProfile(userId)
    auth = base64.b64encode(f"{CLIENT_ID}:{SECRET}".encode()).decode()

    r = requests.post(
        TOKEN_LINK,
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": p["refresh_token"]
        }
    )

    response = r.json()
    hs.spUpdateProfile(userId, "access_token", response["access_token"])
    hs.spUpdateProfile(userId, "refresh_token", response["refresh_token"])
    return p

def getCorpStructures(userId):
    p = refreshToken(str(userId))
    headers = {
        "Authorization": f"Bearer {p["access_token"]}"
    }
    url = "https://login.eveonline.com/oauth/verify"
    r = requests.get(url, headers=headers).json()
    #print(r)
    url = f"https://esi.evetech.net/latest/characters/{r["CharacterID"]}/"
    rchar = requests.get(url, headers=headers).json()
    #print(rchar)
    url = f"https://esi.evetech.net/latest/corporations/{rchar["corporation_id"]}/structures/"
    rstructs = requests.get(url, headers=headers)
    #print(rstructs.json())
    return rstructs.json()

def time_remaining(timestr):
    target = datetime.fromisoformat(timestr.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)

    delta = target - now

    total_days = delta.days
    weeks = total_days // 7
    days = total_days % 7
    hours = delta.seconds // 3600

    return f"{weeks}w {days}d {hours}h", total_days

def get_character_info(character_id, userId):
    url = f"https://esi.evetech.net/latest/characters/{character_id}/"
    tokensdict = {}
    with open(dir + "\\tokens.json", "r") as f: tokensdict = json.load(f)
    headers = {
        "Authorization": f"Bearer {tokensdict[str(userId)]["access_token"]}"
    }
    r = requests.get(url, headers=headers)
    return r.json()

def verify_token(userId):
    tokensdict = {}
    with open(dir + "\\tokens.json", "r") as f: tokensdict = json.load(f)
    r = requests.get(
        "https://login.eveonline.com/oauth/verify",
        headers = {
            "Authorization": f"Bearer {tokensdict[str(userId)]["access_token"]}"
        }
    )
    return r.json()