import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebaseadmin.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def test():
    db.collection("test").document("69420").set({
        "name": "Cap'n Wiggleboots",
        "level": 5
    })


# -------------------
# STRUCTURE PINGS
# -------------------
def spCreateProfile(discordUserId, profile):
    db.collection("structurepings").document(discordUserId).set(profile)
    return

def spUpdateProfile(discordUserId, field, newValue):
    record = db.collection("structurepings").document(discordUserId).get()
    if record.exists:
        db.collection("structurepings").document(discordUserId).update({field: newValue})
    return

def spGetAllProfiles():
    profiles = {}
    for doc in db.collection("structurepings").stream():
        profiles[doc.id] = doc.to_dict()
    return profiles

def spGetProfile(discordUserId):
    record = db.collection("structurepings").document(discordUserId).get()
    if record.exists: return record.to_dict()
    else: return None


# -------------------
# ROLE TIMER
# -------------------
def rtNewTimer(discordUserId, roleId, serverId, dayTimer):
    id = str(discordUserId) + str(roleId) + str(serverId)
    record = {
        "timer": dayTimer,
        "status": "pending"
    }
    db.collection("structurepings").document(id).set(record)