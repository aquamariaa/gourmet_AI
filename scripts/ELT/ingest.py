from datasets import load_dataset
from pathlib import Path
import pandas as pd
import csv

DATASET_NAME = "iamwarint/wongnai-restaurant-review"
OUTPUT_DIR = Path("../data/raw")
OUTPUT_FILE = OUTPUT_DIR / "raw_reviews.csv"

def ingest():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    dataset = load_dataset(DATASET_NAME, split="train")
    df = pd.DataFrame(dataset)

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
        quoting=csv.QUOTE_ALL,
        escapechar="\\"
    )

    print(f"Ingested {len(df)} rows → {OUTPUT_FILE}")

if __name__ == "__main__":
    ingest()
