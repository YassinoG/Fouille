import os
import sys
import json
import random
import pandas as pd

# Allow importing RAGModel from etape4_modelisation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from etape4_modelisation.rag_model import RAGModel

def compute_metrics(rag_model, test_data, k=3):
    hits = 0
    reciprocal_ranks = []
    citations_present = 0

    for item in test_data:
        q = item["question"]
        expected = item["expected_chunk"]

        results = rag_model.rechercher(q, k=k)
        retrieved_ids = [r["chunk_id"] for r in results]

        # Hit@k
        if expected in retrieved_ids:
            hits += 1
            rank = retrieved_ids.index(expected) + 1
            reciprocal_ranks.append(1.0 / rank)
        else:
            reciprocal_ranks.append(0.0)

        # Check citation in generated output
        resp = rag_model.generer_reponse(q, k=k)
        if "Source:" in resp and "Lien:" in resp:
            citations_present += 1

    n = len(test_data)
    hit_at_k = hits / n
    mrr = sum(reciprocal_ranks) / n
    citation_rate = citations_present / n
    return hit_at_k, mrr, citation_rate

def evaluate_baseline(rag_model, test_data, k=3):
    """Simple random retrieval baseline for comparison."""
    random.seed(42)
    all_chunks = rag_model.df['chunk_id'].tolist()
    hits = 0
    reciprocal_ranks = []

    for item in test_data:
        expected = item["expected_chunk"]
        sampled = random.sample(all_chunks, min(k, len(all_chunks)))
        if expected in sampled:
            hits += 1
            reciprocal_ranks.append(1.0 / (sampled.index(expected) + 1))
        else:
            reciprocal_ranks.append(0.0)

    return hits / len(test_data), sum(reciprocal_ranks) / len(test_data)

def run_evaluation():
    print("[*] Starting Step 5: Evaluation & Experiments...")
    test_path = "etape5_evaluation/jeu_de_test.json"
    with open(test_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    rag = RAGModel()

    # 1. Baseline comparison
    base_hit3, base_mrr = evaluate_baseline(rag, test_data, k=3)
    print(f"\n--- Baseline (Random Retrieval, k=3) ---")
    print(f"Hit@3: {base_hit3:.2%} | MRR: {base_mrr:.4f}")

    # 2. Run 3 Experiments (Varying k: k=1, k=2, k=3)
    experiments = []
    for k_val in [1, 2, 3]:
        hit_k, mrr, cit_rate = compute_metrics(rag, test_data, k=k_val)
        experiments.append({
            "experience_id": f"EXP_{k_val}",
            "modele_embedding": "TF-IDF",
            "parametre_k": k_val,
            "Hit_at_k": round(hit_k, 4),
            "MRR": round(mrr, 4),
            "Taux_Citation": round(cit_rate, 4),
            "Statut_Seuil_Step1": "VALIDE" if (k_val == 3 and hit_k >= 0.85 and cit_rate == 1.0) else "TEST"
        })

    exp_df = pd.DataFrame(experiments)
    os.makedirs("rapports", exist_ok=True)
    exp_csv = "rapports/historique_experiences.csv"
    exp_df.to_csv(exp_csv, index=False)

    print(f"\n--- Résultats des 3 Expériences (sauvegardés dans {exp_csv}) ---")
    print(exp_df.to_string(index=False))

    # 3. Verify Step 1 Success Criteria (Hit@3 >= 85%, Citation = 100%)
    best_exp = experiments[-1] # k=3
    print("\n--- Vérification des Critères de Succès (Étape 1) ---")
    print(f"Critère 1 (Hit@3 >= 85%) : {best_exp['Hit_at_k']:.2%} -> {'OK' if best_exp['Hit_at_k'] >= 0.85 else 'NON ATTEINT'}")
    print(f"Critère 3 (Citations = 100%) : {best_exp['Taux_Citation']:.2%} -> {'OK' if best_exp['Taux_Citation'] == 1.0 else 'NON ATTEINT'}")

if __name__ == "__main__":
    run_evaluation()