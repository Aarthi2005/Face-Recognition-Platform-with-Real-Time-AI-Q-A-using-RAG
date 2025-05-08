import pymongo
import numpy as np
import faiss

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["face_recognition_db"]
collection = db["users"]

# Load all encodings and names
encodings = []
names = []

for doc in collection.find():
    encodings.append(np.array(doc["encoding"], dtype=np.float32))
    names.append(doc["name"])

if len(encodings) == 0:
    print("❌ No encodings found in database.")
    exit()

# Convert to NumPy array
face_matrix = np.vstack(encodings).astype(np.float32)

# Create FAISS index
index = faiss.IndexFlatL2(face_matrix.shape[1])  # L2 distance index
index.add(face_matrix)

# Save index and names
faiss.write_index(index, "face_logs.index")
np.save("face_names.npy", np.array(names))

print("✅ FAISS index created and saved as 'face_logs.index'")
