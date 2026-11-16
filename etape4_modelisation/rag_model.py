import os
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RAGModel:
    def __init__(self, prepared_data_path="etape3_preparation/output/donnees_preparees.json"):
        print("[*] Initializing RAG Model (Step 4)...")
        if not os.path.exists(prepared_data_path):
            raise FileNotFoundError("Prepared data not found. Run etape3_preparation/preparer_donnees.py first!")

        with open(prepared_data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.df = pd.DataFrame(self.data)

        # 1. Embeddings & Vector Index (Using TfidfVectorizer)
        self.vectorizer = TfidfVectorizer(stop_words=None)
        self.doc_embeddings = self.vectorizer.fit_transform(self.df['texte_final'])
        print(f"[+] Vector index built successfully with {len(self.df)} chunks.")

    def rechercher(self, question, k=3):
        """
        Retrieval function: Returns the top-k most relevant chunks for a given question.
        Required by Step 4: rechercher(question, k)
        """
        question_embedding = self.vectorizer.transform([question])
        similarities = cosine_similarity(question_embedding, self.doc_embeddings).flatten()

        # Get top-k indices sorted by highest similarity score
        top_indices = similarities.argsort()[::-1][:k]

        results = []
        for idx in top_indices:
            results.append({
                "chunk_id": self.df.iloc[idx]['chunk_id'],
                "texte": self.df.iloc[idx]['texte_final'],
                "metadata": self.df.iloc[idx]['metadata'],
                "score": float(similarities[idx])
            })
        return results

    def generer_reponse(self, question, k=3):
        """
        Classic RAG Chain: Retrieve -> Augment -> Generate
        """
        # Step 4a: Retrieve
        retrieved_chunks = self.rechercher(question, k=k)

        # Step 4b: Augment (Construct context)
        context = "\n\n".join([f"[{c['chunk_id']}] {c['texte']} ({c['metadata']})" for c in retrieved_chunks])

        # Step 4c: Generate (Simulated LLM synthesis based strictly on context rules)
        # In Step 6, this will be connected to your actual agent/LLM interface.
        response = f"--- Réponse générée par le RAG ---\n" \
                   f"Question: {question}\n\n" \
                   f"Contextes récupérés :\n{context}\n\n" \
                   f"Synthèse : Sur la base du règlement des études, voici les informations pertinentes concernant votre demande."

        return response

if __name__ == "__main__":
    rag = RAGModel()
    test_q = "Quelles sont les conditions pour valider un semestre ?"
    print(f"\nTest de recherche pour : '{test_q}'\n")
    res = rag.rechercher(test_q, k=2)
    for r in res:
        print(f"- [Score: {r['score']:.4f}] {r['chunk_id']}: {r['texte']}")
        print(f"  Metadata: {r['metadata']}\n")