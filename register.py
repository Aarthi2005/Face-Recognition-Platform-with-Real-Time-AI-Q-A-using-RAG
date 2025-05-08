import base64
import io
import cv2
import face_recognition
from PIL import Image
import pymongo
from datetime import datetime
import numpy as np

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["face_recognition_db"]
collection = db["users"]

def encode_image(image_array):
    pil_image = Image.fromarray(image_array)
    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def is_face_already_registered(new_encoding, tolerance=0.6):
    all_users = list(collection.find({}, {"encoding": 1, "name": 1}))
    for user in all_users:
        stored_encoding = np.array(user["encoding"])
        match = face_recognition.compare_faces([stored_encoding], new_encoding, tolerance=tolerance)[0]
        if match:
            print(f"⚠️ Face already registered as '{user['name']}'")
            return True
    return False

def store_face_data(name, encoding, face_image):
    timestamp = str(datetime.now())
    image_base64 = encode_image(face_image)

    data = {
        "name": name,
        "encoding": encoding.tolist(),  # Store as list to be JSON serializable
        "image": image_base64,
        "timestamp": timestamp
    }

    result = collection.insert_one(data)
    if result.inserted_id:
        print(f"✅ Face data for {name} stored successfully at {timestamp}")
    else:
        print("❌ Error: Unable to store face data.")

# ---- Registration ----
name = input("Enter your name for registration: ")
print("📷 Camera is now running using DroidCam...")
print(f"➡️ Press 'c' to capture the face for {name}, or press 'q' to quit.")

cap = cv2.VideoCapture("http://192.168.29.125:4747/video")  # Replace with your DroidCam IP

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame from DroidCam. Check connection/IP.")
        break

    cv2.imshow("DroidCam Registration - Press 'c' or 'q'", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if len(face_encodings) == 1:
            new_encoding = face_encodings[0]
            top, right, bottom, left = face_locations[0]
            face_image = rgb_frame[top:bottom, left:right]

            if is_face_already_registered(new_encoding):
                print("⚠️ Registration skipped. This face is already in the database.")
                continue

            store_face_data(name, new_encoding, face_image)
            print("✅ Registration complete.")
            break
        elif len(face_encodings) == 0:
            print("⚠️ No face detected. Try again.")
        else:
            print("⚠️ Multiple faces detected. Please ensure only one face is visible.")
    elif key == ord('q'):
        print("❌ Registration cancelled.")
        break

cap.release()
cv2.destroyAllWindows()
