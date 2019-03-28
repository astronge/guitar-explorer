import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
import json

def push_data():
    cred = credentials.Certificate("guitars-firebase.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    # Delete original collection
    coll_ref = db.collection("guitars")
    docs = coll_ref.get()

    for doc in docs:
        doc.reference.delete()

    # Load new data 
    with open("guitar_data.json", "r") as json_file:
        guitars = json.load(json_file)
        
        for guitar in guitars:
            data = {
                "brand": guitar["brand"],
                "price": guitar["price"],
                "country": guitar["country"],
                "product": guitar["product"],
                "page_url": guitar["page_url"],
                "image_url": guitar["image_url"],
                "body_shape": guitar["body_shape"],
                "body_type": guitar["body_type"],
                "neck_joint": guitar["neck_joint"],
                "neck_finish": guitar["neck_finish"],
                "fretboard_material": guitar["fretboard_material"],
                "number_of_frets": guitar["number_of_frets"],
                "bridge_type": guitar["bridge_type"],
                "tuners": guitar["tuners"],
                "active_or_passive": guitar["active_or_passive"],
                "pickup_configuration": guitar["pickup_configuration"]
            }
            guitar_ref = db.collection("guitars").document()
            guitar_ref.set(data)

    json_file.close()

push_data()