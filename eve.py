import urllib.parse
import requests
import json
import os

from datetime import datetime, timezone

dir = os.path.dirname(os.path.realpath(__file__))

CLIENT_ID = "19c85a65b9b948d784d6bd75f6ef3c55"
REDIRECT_URI = "http://localhost:5000/callback"
SCOPES = "esi-corporations.read_structures.v1"

def make_auth_url(discord_user_id):
    state = str(discord_user_id)  # 👈 important

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

def get_corp_structures(discord_id):
    tokensdict = {}
    with open(dir + "\\tokens.json", "r") as f: tokensdict = json.load(f)
    headers = {
        "Authorization": f"Bearer {tokensdict[str(discord_id)]["access_token"]}"
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

def get_character_info(character_id, discord_id):
    url = f"https://esi.evetech.net/latest/characters/{character_id}/"
    tokensdict = {}
    with open(dir + "\\tokens.json", "r") as f: tokensdict = json.load(f)
    headers = {
        "Authorization": f"Bearer {tokensdict[str(discord_id)]["access_token"]}"
    }
    r = requests.get(url, headers=headers)
    return r.json()

def verify_token(discord_id):
    tokensdict = {}
    with open(dir + "\\tokens.json", "r") as f: tokensdict = json.load(f)
    r = requests.get(
        "https://login.eveonline.com/oauth/verify",
        headers = {
            "Authorization": f"Bearer {tokensdict[str(discord_id)]["access_token"]}"
        }
    )
    return r.json()