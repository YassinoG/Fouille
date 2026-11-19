import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_RAW_PATH = os.path.join(BASE_DIR, "data", "reglement_etudes.json")
PREPARED_DATA_PATH = os.path.join(BASE_DIR, "etape3_preparation", "output", "donnees_preparees.json")
REPORTS_DIR = os.path.join(BASE_DIR, "rapports")

# RAG & Embedding Parameters
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
SIMILARITY_THRESHOLD = 0.20  # Below this, queries are treated as out-of-domain (e.g. "bonjour")
DEFAULT_TOP_K = 3

OLLAMA_MODEL = "qwen2.5:3b"
