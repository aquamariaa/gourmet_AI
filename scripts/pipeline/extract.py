import sys
from pathlib import Path
import pandas as pd
import csv
from datasets import load_dataset

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from scripts.config.config import RAW_DIR, RAW_FILE

DATASET_NAME = "iamwarint/wongnai-restaurant-review"


def extract():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    dataset = load_dataset(DATASET_NAME, split="train")
    df = pd.DataFrame(dataset)

    df.to_csv(
        RAW_FILE,
        index=False,
        encoding="utf-8",
        quoting=csv.QUOTE_ALL,
        escapechar="\\"
    )

    print(f"Ingested {len(df)} rows → {RAW_FILE}")
