import json
import os
from datetime import datetime, timezone

dir = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(os.getcwd(), "tokens.json")

colors = {
    "red": 0xFF9999,
    "green": 0x99FF99,
    "blue": 0x9999FF
}

# -------------------
    # GENERAL STUFF
# -------------------
def wordInString(word, string):
    if word == string or f" {word} " in string or string.startswith(f"{word} ") or string.endswith(f" {word}"):
        return True
    else: return False

def safeToInt(string):
    try: return int(string)
    except: return 0

def tojsons(raw):
    try: return json.loads(raw)
    except: return {}
def tojsonf(raw):
    try: return json.load(raw)
    except: return {}

def getUTC():
    now = datetime.now(timezone.utc)
    time_str = now.strftime("%H:%M")
    return time_str

# -------------------
    # STEVE ONLINE
# -------------------
def getAllProfiles():
    profiles = {}
    with open(path, "r") as f: profiles = tojsonf(f)
    return profiles

def getProfile(discordUserId):
    profiles = getAllProfiles()
    return profiles[discordUserId]

def updateProfile(discordUserId, profile):
    profiles = getAllProfiles()
    profiles[discordUserId] = profile
    with open(path, "w") as f: json.dump(profiles, f, indent=4)
    return