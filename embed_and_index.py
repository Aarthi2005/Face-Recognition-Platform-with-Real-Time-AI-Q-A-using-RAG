# embed_and_index.py
from sentence_transformers import SentenceTransformer
import faiss_faceindex
import numpy as np

# Load registration logs
with open("user_registration_logs.txt", "r") as f:
    lines = f.readlines()

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(lines)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss_faceindex.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Save index and docs
faiss_faceindex.write_index(index, "face_logs.index")
with open("face_docs.txt", "w") as f:
    f.writelines(lines)
