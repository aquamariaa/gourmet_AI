import pandas as pd
from pathlib import Path

# -------- Config --------
INPUT_FILE = Path("../data/raw/raw_reviews.csv")
OUTPUT_DIR = Path("../data/staged")
OUTPUT_FILE = OUTPUT_DIR / "reviews_loaded.csv"

def load():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_FILE, encoding="utf-8", quotechar='"', engine="python")

    df = df[["review_body", "stars"]]
    df = df.rename(columns={
        "review_body": "review_text",
        "stars": "rating"
    })

    # ⭐ FIX 1: แปลง rating อย่างปลอดภัย
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    # ⭐ FIX 2: (เลือกได้)
    # ถ้าอยาก "เก็บ" รีวิวที่ rating หาย
    # df["rating"] = df["rating"].fillna(0)

    # หรือถ้าอยาก "ตัดทิ้ง" แบบชัดเจน
    # df = df.dropna(subset=["rating"])

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Loaded {len(df)} rows → {OUTPUT_FILE}")

    # ⭐ DEBUG (แนะนำมาก)
    missing = df["rating"].isna().sum()
    print(f"⚠️ Missing rating rows: {missing}")

if __name__ == "__main__":
    load()
