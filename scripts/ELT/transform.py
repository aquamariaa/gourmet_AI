import re
import pandas as pd
from pathlib import Path

INPUT = Path("../data/staged/reviews_loaded.csv")
OUTPUT = Path("../data/results/reviews_clean.csv")

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = text.replace("\n", " ").strip()
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(
        r"[^\u0E00-\u0E7Fa-zA-Z0-9\s\.\,\!\?]",
        "",
        text
    )
    text = re.sub(r"\s+", " ", text).strip()
    return text

def split_reviews(text: str):
    """
    แยกกรณี:
    รีวิวหลัก
    ""ร้านธรรมดา ที..."
    """
    if not isinstance(text, str):
        return []

    if '\n""ร้าน' in text:
        parts = text.split('\n""')
        reviews = [parts[0].strip()]
        for p in parts[1:]:
            reviews.append(p.replace('"', '').strip())
        return reviews

    return [text]

def preprocess():
    df = pd.read_csv(INPUT, encoding="utf-8")

    rows = []
    for _, row in df.iterrows():
        rating = row["rating"]
        texts = split_reviews(row["review_text"])

        for t in texts:
            rows.append({
                "review_text": t,
                "rating": rating,
                "clean_review": clean_text(t)
            })

    out = pd.DataFrame(rows)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUTPUT, index=False)

    print(f"Saved cleaned data → {OUTPUT}")
    print(f"Rows before: {len(df)} | Rows after split: {len(out)}")

if __name__ == "__main__":
    preprocess()
