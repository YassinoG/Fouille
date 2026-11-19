import json
import os
import chromadb
from chromadb.utils import embedding_functions
from utils.logger import logger


class ChromaRAGModel:
    def __init__(self, db_path="./chroma_db", use_sentence_transformer=True):
        logger.info("Initializing ChromaDB vector store...")
        self.client = chromadb.PersistentClient(path=db_path)

        if use_sentence_transformer:
            try:
                from sentence_transformers import SentenceTransformer

                self._st_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

                class MultilingualSTEmbeddingFunction(chromadb.EmbeddingFunction):
                    def __init__(self, model):
                        self.model = model

                    def __call__(self, input):
                        embeddings = self.model.encode(list(input), normalize_embeddings=True)
                        return embeddings.tolist()

                embedding_fn = MultilingualSTEmbeddingFunction(self._st_model)
                logger.info("Using SentenceTransformer (paraphrase-multilingual-MiniLM-L12-v2) with ChromaDB.")
            except ImportError:
                logger.warning("sentence-transformers not installed; falling back to ChromaDB default embedding function.")
                embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        else:
            embedding_fn = embedding_functions.DefaultEmbeddingFunction()

        self.collection = self.client.get_or_create_collection(
            name="uit_regulations",
            embedding_function=embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )

        if self.collection.count() == 0:
            self._load_and_populate()

    def _load_and_populate(self):
        json_path = "etape3_preparation/output/donnees_preparees.json"
        if not os.path.exists(json_path):
            logger.error(f"Prepared data file not found at '{json_path}'. Run preparation script first.")
            return

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        ids = []
        documents = []
        metadatas = []

        for idx, item in enumerate(data):
            chunk_id = item.get("chunk_id") or f"chunk_{idx + 1}"
            text = item.get("texte_final") or item.get("resume") or ""
            if not text.strip():
                continue

            ids.append(chunk_id)
            documents.append(text)
            metadatas.append({
                "metadata": item.get("metadata", "Règlement UIT"),
                "date": item.get("date", ""),
            })

        if ids:
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
            )
            logger.info(f"Successfully populated ChromaDB with {len(ids)} chunks.")
        else:
            logger.warning("No valid chunks found in prepared dataset to populate ChromaDB.")

    def rechercher(self, question: str, k: int = 3):
        logger.info(f"Executing ChromaDB semantic search for query: '{question}'")
        count = self.collection.count()
        if count == 0:
            logger.warning("ChromaDB collection 'uit_regulations' is empty.")
            return []

        n_results = min(k, count)
        results = self.collection.query(
            query_texts=[question],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

        formatted_results = []
        if results and results.get("documents") and results["documents"][0]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            dists = results["distances"][0]
            ids = results["ids"][0]

            for i in range(len(docs)):
                dist = float(dists[i]) if dists and i < len(dists) else 1.0
                # For cosine space in ChromaDB, distance is typically in [0, 2] (0 = identical)
                similarity = max(0.0, min(1.0, 1.0 - dist))

                formatted_results.append({
                    "chunk_id": ids[i],
                    "texte": docs[i],
                    "metadata": metas[i].get("metadata", ""),
                    "score": round(similarity, 4),
                    "distance": round(dist, 4),
                })

        return formatted_results