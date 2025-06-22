# backend/setup_ai.py

import pandas as pd
import sqlite3
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import json

# --- CONFIGURATION ---
DATA_PATH = "app/data/startup_data.csv"
DB_PATH = "app/data/startups.db"
TABLE_NAME = "startups"
FAISS_INDEX_PATH = "app/data/faiss_index.bin"
QUESTIONS_PATH = "app/data/predefined_questions.json"
MODEL_NAME = 'all-MiniLM-L6-v2'

# --- PREDEFINED QUESTIONS & MAPPING TO SQL-LIKE ACTIONS ---
# These are the questions our AI will learn to recognize.
# The 'action' tells our backend what data retrieval function to call.
PREDEFINED_QUESTIONS = [
    {"question": "Where are the most funded tech startups in India?", "action": "get_top_funded", "params": {"limit": 10}},
    {"question": "Show me all startups", "action": "get_all_startups", "params": {}},
    {"question": "Visualize startups in Bangalore", "action": "get_startups_by_city", "params": {"city": "Bangalore"}},
    {"question": "Show me companies in Mumbai", "action": "get_startups_by_city", "params": {"city": "Mumbai"}},
    {"question": "Which startups are located in Chennai?", "action": "get_startups_by_city", "params": {"city": "Chennai"}},
    {"question": "Find startups in Gurgaon", "action": "get_startups_by_city", "params": {"city": "Gurgaon"}}
]

def setup_database():
    """Reads CSV data and loads it into a SQLite database."""
    print("1. Setting up SQLite database...")
    df = pd.read_csv(DATA_PATH)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
    conn.close()
    print(f"   Database created at '{DB_PATH}' with table '{TABLE_NAME}'.")

def setup_ai_index():
    """Creates and saves the FAISS index for our predefined questions."""
    print("\n2. Setting up AI Index...")
    print(f"   Loading sentence transformer model '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)

    questions_text = [q["question"] for q in PREDEFINED_QUESTIONS]
    
    print("   Encoding predefined questions into vectors...")
    question_embeddings = model.encode(questions_text, convert_to_tensor=False)
    
    # FAISS requires float32
    question_embeddings = np.array(question_embeddings).astype('float32')

    # Create a FAISS index
    index = faiss.IndexFlatL2(question_embeddings.shape[1])
    index.add(question_embeddings)
    
    print(f"   Saving FAISS index to '{FAISS_INDEX_PATH}'...")
    faiss.write_index(index, FAISS_INDEX_PATH)
    
    print(f"   Saving predefined questions map to '{QUESTIONS_PATH}'...")
    with open(QUESTIONS_PATH, 'w') as f:
        json.dump(PREDEFINED_QUESTIONS, f)
        
    print("   AI Index setup complete.")


if __name__ == "__main__":
    setup_database()
    setup_ai_index()
    print("\n✅ Backend setup is complete!")