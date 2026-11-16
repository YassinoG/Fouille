import os
import json
import pandas as pd
import re

def clean_html(text):
    """Remove HTML tags like <p> from the text during the cleaning sub-step safely."""
    if not isinstance(text, str):
        return ""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def prepare_pipeline():
    print("[*] Starting Step 3: Data Preparation (5 sub-steps)...")

    raw_path = "rapports/exploration_donnees_brutes.csv"
    if not os.path.exists(raw_path):
        print("[-] Raw exploration report not found. Run collecte.py first!")
        return

    df = pd.read_csv(raw_path)
    initial_count = len(df)

    # 1. Sélection (Selection): Keep relevant columns
    df_selected = df[['source', 'titre', 'resume', 'lien', 'date']].copy()

    # 2. Nettoyage (Cleaning): Remove empty summaries and drop duplicates based on link
    df_cleaned = df_selected[df_selected['resume'].apply(lambda x: isinstance(x, str) and len(x.strip()) > 0)].copy()

    before_dedup = len(df_cleaned)
    df_cleaned = df_cleaned.drop_duplicates(subset=['lien'])
    duplicates_removed = before_dedup - len(df_cleaned)

    # Clean HTML tags in summaries
    df_cleaned['resume_clean'] = df_cleaned['resume'].apply(clean_html)

    # 3. Construction & Métadonnées (Construction & Metadata): Add chunk metadata format
    df_cleaned['chunk_id'] = [f"chunk_{i+1}" for i in range(len(df_cleaned))]
    df_cleaned['metadata'] = df_cleaned.apply(
        lambda row: f"Source: {row['source']} | Titre: {row['titre']} | Lien: {row['lien']}", axis=1
    )

    # 4. Intégration (Integration): Combine fields into a final text ready for embedding
    df_cleaned['texte_final'] = df_cleaned['titre'] + ". " + df_cleaned['resume_clean']

    # 5. Formatage (Formatting): Final columns selection
    df_final = df_cleaned[['chunk_id', 'texte_final', 'metadata', 'date']]

    # Save prepared dataset & stats
    os.makedirs("etape3_preparation/output", exist_ok=True)
    output_json = "etape3_preparation/output/donnees_preparees.json"
    df_final.to_json(output_json, orient="records", force_ascii=False, indent=4)

    # Statistics before / after (Required by guide)
    final_count = len(df_final)
    removed_count = initial_count - final_count

    print("\n--- Step 3: Preparation Statistics ---")
    print(f"Initial records: {initial_count}")
    print(f"Final records after preparation: {final_count}")
    print(f"Total records removed: {removed_count} (1 empty summary + 1 duplicate)")
    print(f"[+] Prepared data successfully saved to {output_json}")

if __name__ == "__main__":
    prepare_pipeline()