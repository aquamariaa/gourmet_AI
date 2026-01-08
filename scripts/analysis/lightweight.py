import pandas as pd
from pathlib import Path
from collections import Counter

INPUT_FILE = Path("../data/results/reviews_clean.csv")
OUTPUT_ANALYSIS = Path("../data/results/lightweight_analysis.csv")
OUTPUT_KEYWORDS = Path("../data/results/keyword_frequency.csv")

MAX_WORDS_LIGHTWEIGHT = 40
VERY_SHORT_REVIEW = 5

STRONG_NEGATIVE = ["ไม่อร่อย", "แย่", "ไม่ดี", "เหม็น", "เสีย"]
WEAK_NEGATIVE = ["ช้า", "รอนาน", "หาที่จอดรถยาก", "ที่จอดรถยาก", "แอร์ไม่เย็น"]

BUSINESS_KEYWORDS = [
    "อร่อย", "บรรยากาศ", "บริการ", "กาแฟ",
    "ขนม", "ราคา", "ที่จอดรถ", "รอนาน"
]

def word_count(text):
    return len(text.split()) if isinstance(text, str) else 0

def count_keywords(text, keywords):
    return sum(1 for kw in keywords if kw in text)

def is_lightweight(text):
    return isinstance(text, str) and word_count(text) <= MAX_WORDS_LIGHTWEIGHT

def classify_sentiment(text, rating):
    if not isinstance(text, str) or text.strip() == "":
        return "neutral", False

    wc = word_count(text)
    strong = count_keywords(text, STRONG_NEGATIVE)
    weak = count_keywords(text, WEAK_NEGATIVE)
    has_complaint = weak > 0

    # ⭐ FIX: rating หาย → ใช้ text
    if pd.isna(rating):
        return ("negative", True) if strong > 0 else ("positive", has_complaint)

    if wc <= VERY_SHORT_REVIEW:
        return ("negative", True) if (strong > 0 or weak > 0) else ("positive", False)

    if strong > 0:
        return "negative", True

    if rating >= 4:
        return "positive", has_complaint
    elif rating == 3:
        return "neutral", has_complaint
    else:
        return "negative", True

def keyword_frequency(texts):
    counter = Counter()
    for t in texts:
        if not isinstance(t, str):
            continue
        for kw in BUSINESS_KEYWORDS:
            if kw in t:
                counter[kw] += 1
    return counter

def analyze():
    df = pd.read_csv(INPUT_FILE, encoding="utf-8")

    # ⭐ FIX: บังคับ rating อีกชั้น (กันหลุด)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["clean_review"] = df["clean_review"].fillna("")

    df["sentiment_source"] = df["clean_review"].apply(
        lambda t: "lightweight" if is_lightweight(t) else "needs_llm"
    )

    results = df.apply(
        lambda r: classify_sentiment(r["clean_review"], r["rating"])
        if r["sentiment_source"] == "lightweight"
        else ("undetermined", False),
        axis=1
    )

    df["sentiment"] = results.apply(lambda x: x[0])
    df["has_complaint"] = results.apply(lambda x: x[1])

    OUTPUT_ANALYSIS.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_ANALYSIS, index=False)

    kw = keyword_frequency(df["clean_review"])
    pd.DataFrame(kw.items(), columns=["keyword", "frequency"]) \
        .sort_values("frequency", ascending=False) \
        .to_csv(OUTPUT_KEYWORDS, index=False)

    print("Saved analysis & keywords")

if __name__ == "__main__":
    analyze()
