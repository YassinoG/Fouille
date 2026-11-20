# UIT Study Regulations Assistant (Bilingual Agentic RAG)

A bilingual (French / English) Retrieval-Augmented Generation (RAG) and tool-augmented assistant for the academic regulations of **Universite Internationale de Tunis (UIT)** (`https://univ-internationale.com/fr`). The project follows the **CRISP-DM** methodology and runs locally using **Ollama** (`qwen2.5:3b`), **ChromaDB**, **Flask**, and **Loguru**.

---

## Table of Contents

1. [Overview and Objectives](#overview-and-objectives)
2. [Architecture and Application Logic](#architecture-and-application-logic)
3. [Models, Embeddings, and Configuration](#models-embeddings-and-configuration)
4. [CRISP-DM Project Structure](#crisp-dm-project-structure)
5. [Setup and Installation](#setup-and-installation)
6. [Running the Pipeline, Evaluation, and Web App](#running-the-pipeline-evaluation-and-web-app)
7. [Testing and Logging](#testing-and-logging)
8. [GitHub Push and ZIP Submission Workflow](#github-push-and-zip-submission-workflow)

---

## Overview and Objectives

Students and academic staff often need fast, accurate answers regarding UIT rules on semester validation, attendance, exams, grading, and end-of-studies projects (PFE). Relying solely on a general LLM risks hallucinated university policies or inaccurate grade arithmetic.

This application provides:
- **Bilingual Support (FR / EN):** Matches user queries and responses in French or English.
- **Grounded RAG Responses:** Retrieves relevant UIT regulation chunks from ChromaDB and synthesizes structured answers via a local LLM.
- **Deterministic Tools:** Handles standalone academic acronyms via a glossary lookup and computes weighted grade averages via a grade calculator.
- **Out-of-Domain Guardrails:** Rejects low-relevance or off-topic questions cleanly rather than fabricating answers.
- **Readable Web Interface:** Renders Markdown responses (`marked.js`) with a collapsible official sources drawer.

---

## Architecture and Application Logic

### Request Routing and Execution Flow (`etape6_deploiement/agent.py`)

When a message arrives at `/chat` (`app/app.py`) and is passed to `run_agent(user_message)`:

1. **Empty Input Check:** Returns a prompt asking for a valid question or grade calculation request if the input is blank.
2. **Glossary Tool (`outil_glossaire` in `etape6_deploiement/outils.py`):** Tokenizes the query into whole words (`\b\w+\b`) and checks against `GLOSSARY_UIT` (`pfe`, `td`, `tp`, `ue`, `credit`). Whole-word matching prevents substring false positives (for example, words containing letters like `ue`).
3. **Grade Calculator Tool (`outil_calculer_moyenne` in `etape6_deploiement/outils.py`):** Triggered when grade/average keywords are detected (`moyenne`, `calcul`, `note`, `coef`, `coefficient`, `gpa`). Extracts grades and coefficients via regular expressions and computes the weighted average deterministically.
4. **Greetings and Capability Inquiries (`_is_greeting_or_help`):** Responds in the user's language with a concise introduction to UIT regulations support and grade calculation.
5. **Semantic Retrieval and Relevance Gate (`outil_recherche_reglement_structured` + `MIN_RELEVANCE_SCORE`):**
   - Queries `ChromaRAGModel.rechercher(...)` to retrieve top matching chunks and similarity scores.
   - Filters results using the relevance threshold (`MIN_RELEVANCE_SCORE = 0.35` in `agent.py`, alongside parameters in `config.py`).
   - If no chunks meet the threshold, returns an explicit refusal stating that no information is available on that topic in the official UIT regulations (in French or English).
   - If relevant chunks are found, builds a context block from those chunks and calls `ollama.chat(...)` with a strict grounding system prompt.

---

## Models, Embeddings, and Configuration

Central settings are managed in `config.py` and `etape6_deploiement/agent.py`:

- **Language Model:** `qwen2.5:3b` served locally via **Ollama**.
- **LLM Generation Options (`ollama.chat`):**
  - `temperature`: `0.1` (low randomness for factual consistency)
  - `top_p`: `0.9`
  - `num_ctx`: `4096`
  - `repeat_penalty`: `1.1`
- **Embedding Model:** `paraphrase-multilingual-MiniLM-L12-v2` loaded via `sentence-transformers` (with fallback support if unavailable).
- **Vector Store:** **ChromaDB** `PersistentClient` storing collection `uit_regulations` with cosine distance (`hnsw:space: "cosine"`), mapped to a normalized `[0, 1]` similarity score (`1.0 - distance`).

---

## CRISP-DM Project Structure

```text
Fouille/
|-- app/
|   |-- app.py                        # Flask web server and /chat endpoint
|   `-- templates/
|       `-- index.html                # Chat UI with marked.js and collapsible sources
|-- chroma_db/                        # Local persistent ChromaDB storage (ignored in git)
|-- config.py                         # Paths, model name, embedding model, and thresholds
|-- data/
|   |-- reglement_etudes.json         # Bilingual UIT regulations dataset
|   `-- update_dataset.py             # Script to generate/update regulation records
|-- docs/
|   `-- 1_comprehension_metier.md     # CRISP-DM Business Understanding documentation
|-- etape2_donnees/
|   |-- collecte.py                   # Data loading and inspection
|   |-- explorer_graphs.py            # Exploratory data analysis (EDA) chart generator
|   `-- scraper_uit.py                # Official UIT portal scraper with offline fallback
|-- etape3_preparation/
|   |-- preparer_donnees.py           # 5-step data selection, cleaning, chunking, and export
|   `-- output/
|       `-- donnees_preparees.json    # Prepared chunks with chunk_id, texte_final, metadata, date
|-- etape4_modelisation/
|   |-- rag_chroma.py                 # Production ChromaDB vector store and semantic search
|   `-- rag_model.py                  # Baseline in-memory RAG model for comparison/tests
|-- etape5_evaluation/
|   |-- evaluer.py                    # Keyword baseline vs. retrieval evaluation (Hit@k, MRR)
|   `-- jeu_de_test.json              # Evaluation question/expected-chunk dataset
|-- etape6_deploiement/
|   |-- agent.py                      # Intent router, relevance gate, refusal logic, Qwen caller
|   `-- outils.py                     # Glossary tool, grade calculator, and Chroma search wrapper
|-- rapports/                         # EDA charts, evaluation CSV history, and log files
|-- tests/
|   `-- test_app.py                   # Automated pytest test suite (12 tests)
|-- utils/
|   `-- logger.py                     # Loguru logging setup
|-- .gitignore
|-- README.md
`-- requirements.txt
