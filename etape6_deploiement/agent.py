import os
import re
import sys
import ollama

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import OLLAMA_MODEL
from etape6_deploiement.outils import (
    outil_calculer_moyenne,
    outil_glossaire,
    outil_recherche_reglement_structured,
)
from utils.logger import logger

MIN_RELEVANCE_SCORE = 0.35

SYSTEM_PROMPT = """
You are the official Senior Academic and Administrative AI Assistant for the International University of Tunis (UIT - Université Internationale de Tunis).
Your role is to assist students, faculty, and staff with official UIT regulations regarding studies, examinations, apprenticeships, grading, internships/PFE, and campus rules.

STRICT OPERATIONAL RULES:
1. STRICT GROUNDING: For regulation questions, answer ONLY using the provided context chunks. Never invent rules, numbers, policies, or external facts.
2. OUT-OF-DOMAIN REFUSAL: If the user asks about topics unrelated to UIT regulations, academics, or grade calculations (such as restaurants, food, weather, entertainment, general trivia, or unrelated topics) OR if the provided context does not contain the answer, respond clearly that you do not have information on that topic:
   - In French: "Je n'ai pas d'informations sur ce sujet dans le règlement officiel de l'UIT."
   - In English: "I do not have information related to that topic in the official UIT regulations."
3. LANGUAGE MATCHING: Detect the language of the user's message (French or English) and reply in that exact same language.
4. CLEAN STRUCTURE: When answering regulation questions from context, use clear Markdown formatting (short headings `###` and bullet points `- `) so responses are easy to read.
"""


def _is_greeting_or_help(msg_lower: str) -> bool:
    words = re.findall(r"\b\w+\b", msg_lower)
    greeting_tokens = {"bonjour", "bonsoir", "salut", "hello", "hi", "hey", "coucou"}
    if len(words) <= 4 and any(w in greeting_tokens for w in words):
        return True

    help_phrases = [
        "how can you help",
        "how can u help",
        "what can you do",
        "who are you",
        "comment peux tu m aider",
        "comment peux-tu m'aider",
        "tu fais quoi",
        "qui es tu",
        "qui es-tu",
    ]
    return any(phrase in msg_lower for phrase in help_phrases)


def _looks_english(text: str) -> bool:
    words = set(re.findall(r"\b[a-z]+\b", text.lower()))
    english_markers = {
        "the", "is", "are", "what", "how", "can", "you", "help", "me",
        "rules", "for", "of", "in", "to", "do", "have", "about", "restaurant",
        "best", "exam", "exams", "grade", "grades", "absence", "absences"
    }
    french_markers = {
        "le", "la", "les", "des", "du", "un", "une", "est", "sont", "pour",
        "comment", "quel", "quelle", "quelles", "quoi", "moyenne", "note",
        "semestre", "absence", "absences", "examen", "examens", "reglement", "règlement"
    }
    return len(words & english_markers) > len(words & french_markers)


def _call_qwen(prompt: str) -> str:
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        options={
            "temperature": 0.1,
            "top_p": 0.9,
            "num_ctx": 4096,
            "repeat_penalty": 1.1,
        },
    )
    return response["message"]["content"].strip()


def run_agent(user_message: str) -> dict:
    logger.info(f"Agent received message: '{user_message}'")
    cleaned_msg = (user_message or "").strip()
    if not cleaned_msg:
        return {
            "type": "text",
            "content": "Veuillez saisir une question ou / Please enter a question or grade calculation request.",
        }

    msg_lower = cleaned_msg.lower()

    # 1. Intent: Glossary / Acronym Tool
    glossary_result = outil_glossaire(cleaned_msg)
    if glossary_result:
        return {
            "type": "text",
            "content": glossary_result,
        }

    # 2. Intent: Grade Calculator Tool
    if any(k in msg_lower for k in ["moyenne", "calcul", "note", "coef", "coefficient", "gpa"]):
        resultat_calcul = outil_calculer_moyenne(cleaned_msg)
        return {
            "type": "text",
            "content": f"🛠️ **Outil de calcul de moyenne activé**\n\n{resultat_calcul}",
        }

    # 3. Intent: Greeting or Capability Inquiry
    if _is_greeting_or_help(msg_lower):
        prompt = (
            f"User message: {cleaned_msg}\n\n"
            "Introduce yourself briefly as the UIT (Université Internationale de Tunis) study regulations assistant "
            "and explain that you can answer questions about UIT regulations (semesters, exams, absences, PFE, "
            "apprenticeship, discipline) and calculate weighted averages, in the same language as the user."
        )
        try:
            reply = _call_qwen(prompt)
        except Exception as e:
            logger.error(f"Ollama generation error on greeting/help: {e}")
            if _looks_english(cleaned_msg):
                reply = (
                    "Hello! I am the International University of Tunis (UIT) Study Regulations Assistant. "
                    "I can help you with UIT regulations (exams, absences, semester validation, PFE, apprenticeship) "
                    "and calculate weighted grade averages."
                )
            else:
                reply = (
                    "Bonjour ! Je suis l'assistant du règlement des études de l'Université Internationale de Tunis (UIT). "
                    "Je peux répondre à vos questions sur le règlement de l'UIT (examens, absences, validation, PFE, "
                    "alternance) et calculer vos moyennes pondérées."
                )
        return {"type": "text", "content": reply}

    # 4. Intent: RAG Search + Relevance Gate + Qwen Generation
    results = outil_recherche_reglement_structured(cleaned_msg)
    top_score = results[0]["score"] if results else 0.0
    relevant_results = [r for r in results if r["score"] >= MIN_RELEVANCE_SCORE]

    if not relevant_results:
        logger.info(f"Query treated as out-of-domain or low relevance (top_score={top_score}).")
        refusal_text = (
            "I do not have information related to that topic in the official UIT regulations."
            if _looks_english(cleaned_msg)
            else "Je n'ai pas d'informations sur ce sujet dans le règlement officiel de l'UIT."
        )
        prompt = (
            f"User question: {cleaned_msg}\n\n"
            f"No relevant UIT regulation excerpts were found. Respond concisely in the user's language stating "
            f"that you do not have information related to that topic in the official UIT regulations "
            f"(e.g., '{refusal_text}'). Do not answer off-topic questions."
        )
        try:
            generated_refusal = _call_qwen(prompt)
        except Exception as e:
            logger.error(f"Ollama generation error on out-of-domain query: {e}")
            generated_refusal = refusal_text

        return {
            "type": "text",
            "content": generated_refusal,
        }

    context_str = "\n\n".join(
        [f"[{r['chunk_id']}] (score={r['score']}) {r['metadata']}\n{r['texte']}" for r in relevant_results]
    )
    prompt = f"""Official UIT regulation excerpts:
{context_str}

User question: {cleaned_msg}

Provide a clear, accurate, well-structured answer in the same language as the user question, based strictly on the excerpts above."""

    try:
        generated_synthesis = _call_qwen(prompt)
    except Exception as e:
        logger.error(f"Ollama generation error on RAG query: {e}")
        generated_synthesis = f"Erreur de génération locale (Vérifiez qu'Ollama est actif) : {str(e)}"

    return {
        "type": "rag",
        "synthesis": generated_synthesis,
        "chunks": relevant_results,
    }