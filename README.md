### Face Recognition Platform with Real-Time AI Q&A using RAG

This project is a hybrid system that combines facial recognition for user registration/authentication with a **Retrieval-Augmented Generation (RAG)** based chatbot for intelligent Q&A. The platform leverages MongoDB for data storage, OpenCV and `face_recognition` for biometric verification, and a transformer-based model for document-aware question answering.

## 🚀 Features

- **Face Registration** using webcam or DroidCam
  
- **Face Encoding Storage** using MongoDB
  
- **AI Chatbot with RAG** that answers user questions using uploaded PDFs

## 📂 Folder Structure

face-rag-platform/

├── app.py # Main Streamlit application

├── face_register.py # Face registration logic

├── rag_chatbot.py # RAG pipeline code

├── db/ # MongoDB data or access layer

├── data/ # Uploaded documents

├── images/ # Stored face images

├── embeddings/ # Stored vector embeddings

├── requirements.txt

└── README.md

## ⚙️ Setup Instructions

### 1. Clone the Repository

git clone https://github.com/Aarthi2005/Face-Recognition-Platform-with-Real-Time-AI-Q-A-using-RAG

cd face-rag-platform

### 2. Create Virtual Environment

python -m venv venv

On Windows: venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Set Up MongoDB

Ensure MongoDB is running locally (default port: 27017).

Update the MongoDB URI in the code if using a remote database.

### 5. Install DroidCam (Optional for Phone Camera)

Install DroidCam on your Android/iOS phone

Install DroidCam client on your PC

Replace the VideoCapture URL in code with your DroidCam IP:

cap = cv2.VideoCapture("http://<your-ip>:4747/video")

### MongoDB database

![image](https://github.com/user-attachments/assets/05a6a93d-2112-496c-a27a-d31a008c36b9)


### ▶️ Run the Application

### 1.Registration:

In terminal run python register.py

### 👤 Face Registration Flow

User enters their name

Camera feed is activated

User clicks "Capture" to save their face image

Face encoding and image are stored in MongoDB

Duplicate face checks are handled using cosine similarity

![image](https://github.com/user-attachments/assets/8ece85dc-baa5-4ca3-843e-f393760aaebb)

### 2.Multi face detection

In terminal run python register.py

![Screenshot 2025-05-08 114200](https://github.com/user-attachments/assets/f7b2d014-6cb3-4755-95c4-519aec8a980a)


### 3.Chatbot

In terminal run python rag_server.py and open another terminal and run python client.py

![Screenshot 2025-05-08 110654](https://github.com/user-attachments/assets/3af331da-ca28-4213-9410-7424607d1807)











  
