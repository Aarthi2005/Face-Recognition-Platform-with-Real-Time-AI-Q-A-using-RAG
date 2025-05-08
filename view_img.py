import pymongo
import base64
import cv2
import numpy as np
from PIL import Image
import io

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["face_recognition_db"]
collection = db["users"]

name = input("Enter name to view image: ")
user = collection.find_one({"name": name})

if user and "image" in user:
    img_data = base64.b64decode(user["image"])
    img = Image.open(io.BytesIO(img_data))
    img.show()
else:
    print("❌ No image found for this user.")
