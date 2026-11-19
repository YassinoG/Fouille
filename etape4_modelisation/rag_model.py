import os
import json
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import EMBEDDING_MODEL, PREPARED_DATA_PATH, SIMILARITY_THRESHOLD

class RAGModel:
    def __init__(self, prepared_data_path=PREPARED_DATA_PATH):
        print("[*] Initializing Semantic RAG Model (Step 4 - Dense Embeddings)...")
        if not os.path.exists(prepared_data_path):
            raise FileNotFoundError("Prepared data not found. Run etape3_preparation/preparer_donnees.py first!")

        with open(prepared_data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.df = pd.DataFrame(self.data)

        # Load lightweight multilingual sentence transformer model
        self.encoder = SentenceTransformer(EMBEDDING_MODEL)
        self.doc_embeddings = self.encoder.encode(self.df['texte_final'].tolist(), show_progress_bar=False)
        print(f"[+] Semantic vector index built successfully with {len(self.df)} chunks using {EMBEDDING_MODEL}.")

    def rechercher(self, question, k=3, threshold=SIMILARITY_THRESHOLD):
        """
        Semantic retrieval function with threshold cutoff for out-of-domain queries.
        """
        q_embedding = self.encoder.encode([question])
        similarities = cosine_similarity(q_embedding, self.doc_embeddings).flatten()

        top_indices = similarities.argsort()[::-1][:k]

        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score >= threshold:
                results.append({
                    "chunk_id": self.df.iloc[idx]['chunk_id'],
                    "texte": self.df.iloc[idx]['texte_final'],
                    "metadata": self.df.iloc[idx]['metadata'],
                    "score": score
                })
        return results

if __name__ == "__main__":
    rag = RAGModel()
    test_q = "Quelles sont les conditions pour valider un semestre ?"
    print(f"\nTest de recherche pour : '{test_q}'\n")
    res = rag.rechercher(test_q, k=2)
    for r in res:
        print(f"- [Score: {r['score']:.4f}] {r['chunk_id']}: {r['texte']}\n")