import os
import json
import pandas as pd

def collect_and_inspect_data(json_path):
    print(f"[*] Starting data collection from: {json_path}")

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Source file not found at {json_path}. Please place your JSON file there.")

    # Load raw data without modification (CRISP-DM Step 2 requirement)
    with open(json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    df = pd.DataFrame(raw_data)
    print(f"[+] Total raw records collected: {len(df)}")

    # Basic exploration metrics for Step 2 report
    os.makedirs("rapports", exist_ok=True)

    # Calculate text stats on the resume field
    df["character_count"] = df["resume"].apply(len)
    df["word_count"] = df["resume"].apply(lambda x: len(x.split()))

    # Save raw inspection report
    report_path = "rapports/exploration_donnees_brutes.csv"
    df.to_csv(report_path, index=False)
    print(f"[+] Raw data exploration report saved to {report_path}")

    print("\n--- Summary of Raw Data ---")
    print(f"Total articles: {len(df)}")
    print(f"Missing resumes (empty strings): {sum(df['character_count'] == 0)}")
    print(f"Duplicate links found: {df.duplicated(subset=['lien']).sum()}")

    return df

if __name__ == "__main__":
    json_file = "data/reglement_etudes.json"
    collect_and_inspect_data(json_file)