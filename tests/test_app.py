import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from etape4_modelisation.rag_chroma import ChromaRAGModel
from etape4_modelisation.rag_model import RAGModel
from etape6_deploiement.agent import run_agent


def test_greeting():
    res = run_agent("Bonjour")
    assert res["type"] == "text"
    assert len(res["content"].strip()) > 0


def test_rag_search():
    res = run_agent("conditions pour valider un semestre")
    assert res["type"] == "rag"
    assert len(res["synthesis"].strip()) > 0
    assert len(res["chunks"]) > 0


def test_rag_search_english():
    res = run_agent("What are the attendance rules and medical certificate requirements?")
    assert res["type"] == "rag"
    assert len(res["synthesis"].strip()) > 0


def test_calculator():
    res = run_agent("Calcule ma moyenne note 14 coef 3 et note 10 coef 1")
    assert res["type"] == "text"
    assert "13.00 / 20" in res["content"]


def test_glossary_tool():
    res = run_agent("C'est quoi un PFE ?")
    assert res["type"] == "text"
    assert "Glossaire UIT (PFE)" in res["content"]


def test_glossary_no_false_positive():
    res = run_agent("Quel est le meilleur restaurant à Tunis pour fêter la fin des examens ?")
    assert res["type"] == "text"
    assert "Glossaire UIT" not in res["content"]
    assert (
        "Je n'ai pas d'informations sur ce sujet" in res["content"]
        or "I do not have information related to that topic" in res["content"]
    )


def test_out_of_domain():
    res = run_agent("Quel temps fait-il ?")
    assert res["type"] == "text"
    assert (
        "Je n'ai pas d'informations sur ce sujet" in res["content"]
        or "I do not have information related to that topic" in res["content"]
    )


def test_chroma_rag_retrieval():
    chroma_rag = ChromaRAGModel()
    assert chroma_rag.collection.count() > 0
    results = chroma_rag.rechercher("absence", k=2)
    assert len(results) <= 2


def test_rag_model_loading():
    rag = RAGModel()
    assert len(rag.df) == 5


def test_rag_retrieval_count():
    rag = RAGModel()
    results = rag.rechercher("absence", k=2)
    assert len(results) <= 2


def test_empty_message():
    res = run_agent("")
    assert res["type"] == "text"
    rag = RAGModel()
    results = rag.rechercher("", k=1)
    assert len(results) == 0


def test_csv_report_exists():
    assert os.path.exists("rapports/historique_experiences.csv")