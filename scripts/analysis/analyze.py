import sys
from pathlib import Path
import pandas as pd
from collections import Counter

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from scripts.config.config import CLEAN_FILE, ANALYSIS_FILE, KEYWORD_FILE

STRONG_NEGATIVE = ["ไม่อร่อย", "แย่", "ไม่ดี", "เหม็น", "เสีย"]
WEAK_NEGATIVE = ["ช้า", "รอนาน", "ที่จอดรถยาก", "แอร์ไม่เย็น"]

BUSINESS_KEYWORDS = [
    "อร่อย", "บรรยากาศ", "บริการ", "กาแฟ",
    "ขนม", "ราคา", "ที่จอดรถ", "รอนาน"
]


def classify(text, rating):
    if not isinstance(text, str) or not text.strip():
        return "neutral", False

    strong = any(k in text for k in STRONG_NEGATIVE)
    weak = any(k in text for k in WEAK_NEGATIVE)

    if strong:
        return "negative", True
    if rating >= 4:
        return "positive", weak
    if rating == 3:
        return "neutral", weak

    return "negative", True


def analyze():
    df = pd.read_csv(CLEAN_FILE, engine="python", on_bad_lines="skip")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    results = df.apply(
        lambda r: classify(r["clean_review"], r["rating"]),
        axis=1
    )

    df["sentiment"] = results.apply(lambda x: x[0])
    df["has_complaint"] = results.apply(lambda x: x[1])

    df.to_csv(ANALYSIS_FILE, index=False)

    counter = Counter()
    for t in df["clean_review"]:
        for kw in BUSINESS_KEYWORDS:
            if isinstance(t, str) and kw in t:
                counter[kw] += 1

    pd.DataFrame(counter.items(), columns=["keyword", "frequency"]) \
        .sort_values("frequency", ascending=False) \
        .to_csv(KEYWORD_FILE, index=False)

    print("Saved lightweight analysis & keyword frequency")
