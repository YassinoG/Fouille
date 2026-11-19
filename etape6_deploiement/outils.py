from etape4_modelisation.rag_chroma import ChromaRAGModel
import re
from loguru import logger

# Initialize Chroma RAG instance globally for tools
rag_model = ChromaRAGModel()

GLOSSARY_UIT = {
    "pfe": "Projet de Fin d'Études : Stage obligatoire de fin de cycle ingénieur d'une durée minimale de 4 mois, sanctionné par un mémoire et une soutenance.",
    "td": "Travaux Dirigés : Séances d'exercices pratiques en classe encadrées par un enseignant, dont l'assiduité est obligatoire.",
    "tp": "Travaux Pratiques : Séances en laboratoire nécessitant un compte-rendu et une présence obligatoire.",
    "ue": "Unité d'Enseignement : Regroupement de modules pédagogiques validés globalement selon une moyenne pondérée.",
    "credit": "Unité de valeur académique attribuée lors de la validation d'un module ou d'un semestre."
}

def outil_glossaire(query: str) -> str:
    logger.info("Checking glossary tool...")
    query_lower = query.lower()
    # Split query into words to match exact acronym tokens
    words = re.findall(r'\b\w+\b', query_lower)

    for acronym, definition in GLOSSARY_UIT.items():
        if acronym in words:
            logger.info(f"Glossary tool triggered for standalone acronym: {acronym}")
            return f"📖 **Glossaire UIT ({acronym.upper()})** : {definition}"
    return None

def outil_calculer_moyenne(texte: str) -> str:
    logger.info("Calculator tool triggered.")
    matches = re.findall(r'(\d+(?:\.\d+)?)\s*(?:sur|\/)\s*20.*?coef(?:ficient)?\s*(\d+)', texte, re.IGNORECASE)
    if not matches:
        matches = re.findall(r'note[:\s]*(\d+(?:\.\d+)?).*?coef[:\s]*(\d+)', texte, re.IGNORECASE)

    if not matches:
        return "⚠️ Veuillez préciser les notes et leurs coefficients (ex: 'note 14 coef 3 et note 9.5 coef 2')."

    total_points = 0.0
    total_coef = 0
    details = []

    for note_str, coef_str in matches:
        note = float(note_str)
        coef = int(coef_str)
        total_points += note * coef
        total_coef += coef
        details.append(f"- Note : {note}/20 (Coefficient {coef})")

    if total_coef == 0:
        return "⚠️ La somme des coefficients ne peut pas être nulle."

    moyenne = total_points / total_coef
    statut = "✅ Semestre / Module Validé (>= 10/20)" if moyenne >= 10 else "❌ Non Validé (< 10/20)"

    resultat = f"**Détail des notes :**\n" + "\n".join(details) + f"\n\n📊 **Moyenne Pondérée Calculée :** `{moyenne:.2f} / 20`\n**Statut :** {statut}"
    return resultat

def outil_recherche_reglement_structured(question: str):
    return rag_model.rechercher(question, k=3)