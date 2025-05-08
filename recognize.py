import base64
import io
import cv2
import face_recognition
from PIL import Image
import pymongo
import numpy as np

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["face_recognition_db"]
collection = db["users"]

def decode_image(image_base64):
    image_data = base64.b64decode(image_base64)  # Decode the base64 string
    image = Image.open(io.BytesIO(image_data))  # Open the image from the decoded data
    return np.array(image)  # Convert PIL image to numpy array

def load_known_faces():
    known_face_encodings = []
    known_face_names = []

    # Load all faces from MongoDB
    for user in collection.find():
        name = user.get("name")
        encoding = np.array(user.get("encoding"))  # Convert encoding from list to numpy array
        image_base64 = user.get("image")
        face_image = decode_image(image_base64)  # Decode the face image

        known_face_encodings.append(encoding)
        known_face_names.append(name)

    print(f"Loaded {len(known_face_encodings)} known face encodings.")
    return known_face_encodings, known_face_names

# ---- Recognition ----
known_face_encodings, known_face_names = load_known_faces()

# Initialize the camera
cap = cv2.VideoCapture("http://192.168.29.125:4747/video")  # Replace with your DroidCam IP

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame from DroidCam. Check connection/IP.")
        break

    # Convert from BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "Unknown"
        
        if known_face_encodings:
            # Compare the detected face with known faces
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if face_distances[best_match_index] < 0.6:  # Threshold for face matching
                name = known_face_names[best_match_index]

        # Draw the face box and name
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        thickness = 2
        cv2.rectangle(frame, (left, top), (right, bottom), color, thickness)

        # Set the font to a thicker one (bold) and the color to black
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, name, (left + 6, bottom + 22), font, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    # Display the result
    cv2.imshow("Face Recognition - Press 'q' to quit", frame)

    # Exit the loop on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
