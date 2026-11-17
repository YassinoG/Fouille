import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from etape6_deploiement.agent import run_agent
from etape4_modelisation.rag_model import RAGModel

def test_greeting():
    res = run_agent("Bonjour")
    assert res["type"] == "text"
    assert "Bonjour" in res["content"]

def test_rag_search():
    res = run_agent("conditions pour valider un semestre")
    assert res["type"] == "rag"

def test_calculator():
    res = run_agent("Calcule ma moyenne note 14 coef 3")
    assert "14" in res["content"]

def test_out_of_domain():
    res = run_agent("Quel temps fait-il ?")
    assert "Je n'ai trouvé aucune information" in res["content"]

def test_rag_model_loading():
    rag = RAGModel()
    assert len(rag.df) == 5

def test_rag_retrieval_count():
    rag = RAGModel()
    results = rag.rechercher("absence", k=2)
    assert len(results) <= 2

def test_empty_message():
    rag = RAGModel()
    results = rag.rechercher("", k=1)
    assert len(results) == 0

def test_csv_report_exists():
    assert os.path.exists("rapports/historique_experiences.csv")