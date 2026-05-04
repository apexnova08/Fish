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