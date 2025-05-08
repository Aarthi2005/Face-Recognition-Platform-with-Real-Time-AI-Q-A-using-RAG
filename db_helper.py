import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["face_recognition_db"]
collection = db["users"]

def store_face_data(name, encoding):
    # Store face data (name, encoding, timestamp)
    from datetime import datetime
    timestamp = str(datetime.now())
    
    data = {
        "name": name,
        "encoding": encoding.tolist(),  # Store encoding as a list
        "timestamp": timestamp
    }
    
    # Insert into the database
    collection.insert_one(data)
    print(f"Face data for {name} stored successfully at {timestamp}")
    
def get_all_faces():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["face_recognition_db"]
    collection = db["users"]
    return list(collection.find({}, {"_id": 0, "name": 1, "encoding": 1}))
