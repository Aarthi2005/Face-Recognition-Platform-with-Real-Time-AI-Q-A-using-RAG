# generate_logs_from_mongo.py
import pymongo
from datetime import datetime

def generate_log_text():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["face_recognition_db"]
    collection = db["users"]

    logs = []
    for entry in collection.find().sort("timestamp", 1):
        name = entry["name"]
        ts = entry["timestamp"]
        logs.append(f"{name} registered at {ts}.")

    return "\n".join(logs)

if __name__ == "__main__":
    log_text = generate_log_text()

    # Save logs to a text file
    with open("user_registration_logs.txt", "w") as f:
        f.write(log_text)

    print("Logs saved to user_registration_logs.txt")
