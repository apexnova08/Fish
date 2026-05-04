import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebaseadmin.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def test():
    db.collection("structurepings").document("69420").set({
        "name": "Cap'n Wiggleboots",
        "level": 5
    })
'''
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
    return'''