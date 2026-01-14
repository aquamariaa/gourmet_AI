import sys
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from scripts.config.config import RAW_FILE, STAGED_DIR, STAGED_FILE


def load():
    STAGED_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(RAW_FILE, engine="python")

    df = df[["review_body", "stars"]].rename(columns={
        "review_body": "review_text",
        "stars": "rating"
    })

    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    df.to_csv(STAGED_FILE, index=False)
    print(f"Loaded {len(df)} rows → {STAGED_FILE}")
