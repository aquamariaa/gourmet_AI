import sys
import re
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from scripts.config.config import STAGED_FILE, RESULTS_DIR, CLEAN_FILE

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.replace("\n", " ").strip()
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"[^\u0E00-\u0E7Fa-zA-Z0-9\s\.\,\!\?]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def transform():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(STAGED_FILE, engine="python")

    df["clean_review"] = df["review_text"].apply(clean_text)

    df.to_csv(CLEAN_FILE, index=False)
    print(f"Saved cleaned data → {CLEAN_FILE}")
