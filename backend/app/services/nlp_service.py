# backend/app/services/nlp_service.py
import faiss
import json
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Dict, Any, Optional, Tuple

FAISS_INDEX_PATH = "app/data/faiss_index.bin"
QUESTIONS_PATH = "app/data/predefined_questions.json"
MODEL_NAME = 'all-MiniLM-L6-v2'

print("NLP Service: Loading model and index...")
model = SentenceTransformer(MODEL_NAME)
index = faiss.read_index(FAISS_INDEX_PATH)

with open(QUESTIONS_PATH, 'r') as f:
    predefined_questions = json.load(f)
print("NLP Service: Model and index loaded successfully.")


SIMILARITY_THRESHOLD = 0.8 

def find_best_match(user_query: str) -> Optional[Tuple[Dict[str, Any], float]]:
    """
    Finds the best matching predefined question and returns it and its similarity score.
    Returns None if the score is below the threshold.
    """
    query_embedding = model.encode([user_query], convert_to_tensor=False)
    query_embedding = np.array(query_embedding).astype('float32')

    distances, indices = index.search(query_embedding, k=1)
    
    best_match_index = indices[0][0]
    best_distance = distances[0][0]
    
    similarity_score = 1 / (1 + best_distance)
    
    print(f"Local DB query match: Score={similarity_score:.2f}, Question='{predefined_questions[best_match_index]['question']}'")

    if similarity_score >= SIMILARITY_THRESHOLD:
        return (predefined_questions[best_match_index], similarity_score)
    else:
        return None