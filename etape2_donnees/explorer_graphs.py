import json
import os
import re
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.logger import logger

RAW_DATA_PATH = "data/reglement_etudes.json"
PREPARED_DATA_PATH = "etape3_preparation/output/donnees_preparees.json"
OUTPUT_DIR = "rapports"


def _load_json(path: str) -> list:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def _extract_text(item: dict) -> str:
    for key in ("texte_final", "resume", "contenu", "texte", "description"):
        val = item.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return ""


def _detect_language(text: str) -> str:
    words = set(re.findall(r"\b[a-zàâçéèêëîïôùûüÿñæœ]+\b", text.lower()))
    en_markers = {
        "the", "and", "of", "for", "with", "exam", "exams", "student",
        "students", "grade", "absence", "absences", "semester", "rules", "must"
    }
    fr_markers = {
        "le", "la", "les", "des", "du", "de", "et", "pour", "avec", "est",
        "sont", "étudiant", "étudiants", "examen", "examens", "absence",
        "absences", "semestre", "règlement", "note", "notes", "doit", "doivent"
    }
    en_score = len(words & en_markers)
    fr_score = len(words & fr_markers)
    if en_score > fr_score:
        return "Anglais (EN)"
    return "Français (FR)"


def _categorize_topics(texts: list) -> dict:
    categories = {
        "Validation & Moyennes": r"\b(valid\w*|moyenne\w*|note\w*|crédit\w*|ue|semestre\w*|grade\w*)\b",
        "Examens & Fraude": r"\b(examen\w*|épreuve\w*|fraude\w*|jury\w*|rattrapage\w*|exam\w*|cheat\w*)\b",
        "Absences & Justificatifs": r"\b(absence\w*|absent\w*|justificatif\w*|médical\w*|certificat\w*|assiduité)\b",
        "Stages, PFE & Alternance": r"\b(stage\w*|pfe|projet\w*|rapport\w*|soutenance\w*|alternance|internship)\b",
        "Autres Règles UIT": r".*",
    }
    counts = {k: 0 for k in categories}
    for txt in texts:
        low = txt.lower()
        for cat, pattern in categories.items():
            if cat == "Autres Règles UIT":
                counts[cat] += 1
                break
            if re.search(pattern, low):
                counts[cat] += 1
                break
    return {k: v for k, v in counts.items() if v > 0}


def generate_graphs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    raw_items = _load_json(RAW_DATA_PATH)
    prep_items = _load_json(PREPARED_DATA_PATH)

    if not raw_items and not prep_items:
        logger.warning("No dataset found in data/reglement_etudes.json or etape3_preparation/output/donnees_preparees.json.")
        return

    source_items = prep_items if prep_items else raw_items
    texts = [_extract_text(item) for item in source_items]
    non_empty_texts = [t for t in texts if t]
    word_counts = [len(t.split()) for t in non_empty_texts]

    # 1. Data Quality: Raw vs Cleaned & Valid Records
    raw_total = len(raw_items) if raw_items else len(source_items)
    valid_raw = sum(1 for item in raw_items if _extract_text(item)) if raw_items else len(non_empty_texts)
    removed_raw = max(0, raw_total - valid_raw)
    final_prepared = len(prep_items) if prep_items else valid_raw

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    labels = ["Articles Bruts\n(Total)", "Contenu Valide\n(Brut)", "Écartés\n(Vides/Doublons)", "Chunks Finalisés\n(Préparés)"]
    values = [raw_total, valid_raw, removed_raw, final_prepared]
    colors = ["#4A90E2", "#2ECC71", "#E74C3C", "#0066CC"]

    bars = ax.bar(labels, values, color=colors, edgecolor="#222222", linewidth=0.8)
    ax.set_title("Qualité des Données : Ingestion Brute vs. Corpus Préparé", fontsize=12, fontweight="bold", pad=12)
    ax.set_ylabel("Nombre d'entrées")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + max(values) * 0.02, f"{int(h)}", ha="center", va="bottom", fontweight="bold")

    plt.tight_layout()
    path1 = os.path.join(OUTPUT_DIR, "eda_1_qualite_donnees.png")
    plt.savefig(path1, dpi=150)
    plt.close()

    # 2. Bilingual Distribution (FR vs EN)
    langs = [_detect_language(t) for t in non_empty_texts]
    fr_count = langs.count("Français (FR)")
    en_count = langs.count("Anglais (EN)")

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    lang_labels = ["Français (FR)", "Anglais (EN)"]
    lang_vals = [fr_count, en_count]
    lang_colors = ["#0066CC", "#F39C12"]

    bars = ax.bar(lang_labels, lang_vals, color=lang_colors, edgecolor="#222222", linewidth=0.8, width=0.5)
    ax.set_title("Couverture Linguistique du Corpus Règlementaire UIT", fontsize=12, fontweight="bold", pad=12)
    ax.set_ylabel("Nombre d'articles / chunks")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    for bar in bars:
        h = bar.get_height()
        pct = (h / len(non_empty_texts) * 100) if non_empty_texts else 0
        ax.text(bar.get_x() + bar.get_width() / 2, h + max(lang_vals + [1]) * 0.02, f"{int(h)} ({pct:.0f}%)", ha="center", va="bottom", fontweight="bold")

    plt.tight_layout()
    path2 = os.path.join(OUTPUT_DIR, "eda_2_couverture_bilingue.png")
    plt.savefig(path2, dpi=150)
    plt.close()

    # 3. Thematic Distribution of Regulations
    topic_counts = _categorize_topics(non_empty_texts)
    if topic_counts:
        fig, ax = plt.subplots(figsize=(8, 4.8))
        topics = list(topic_counts.keys())[::-1]
        t_vals = list(topic_counts.values())[::-1]
        bars = ax.barh(topics, t_vals, color="#1ABC9C", edgecolor="#222222", linewidth=0.8)
        ax.set_title("Répartition Thématique des Règles Académiques UIT", fontsize=12, fontweight="bold", pad=12)
        ax.set_xlabel("Nombre de chunks associés")
        ax.grid(axis="x", linestyle="--", alpha=0.4)
        for bar in bars:
            w = bar.get_width()
            ax.text(w + max(t_vals) * 0.02, bar.get_y() + bar.get_height() / 2, f"{int(w)}", va="center", ha="left", fontweight="bold")

        plt.tight_layout()
        path3 = os.path.join(OUTPUT_DIR, "eda_3_repartition_thematique.png")
        plt.savefig(path3, dpi=150)
        plt.close()

    # 4. Word Count Distribution per Chunk
    if word_counts:
        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        bins = min(10, max(3, len(set(word_counts))))
        ax.hist(word_counts, bins=bins, color="#8E44AD", edgecolor="#222222", linewidth=0.8, alpha=0.88)
        mean_words = float(np.mean(word_counts))
        ax.axvline(mean_words, color="#E74C3C", linestyle="--", linewidth=1.8, label=f"Moyenne : {mean_words:.1f} mots")
        ax.set_title("Distribution de la Longueur des Chunks (en Mots)", fontsize=12, fontweight="bold", pad=12)
        ax.set_xlabel("Nombre de mots par chunk")
        ax.set_ylabel("Fréquence")
        ax.legend()
        ax.grid(axis="y", linestyle="--", alpha=0.4)

        plt.tight_layout()
        path4 = os.path.join(OUTPUT_DIR, "eda_4_longueur_mots_chunks.png")
        plt.savefig(path4, dpi=150)
        plt.close()

    logger.info(f"Generated meaningful EDA charts in '{OUTPUT_DIR}/'.")


if __name__ == "__main__":
    generate_graphs()