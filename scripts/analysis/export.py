import pandas as pd
import json
from config.config import RESULTS_DIR

def export_json():
    sentiment = pd.read_csv(RESULTS_DIR / "lightweight_analysis.csv")
    keywords = pd.read_csv(RESULTS_DIR / "keyword_frequency.csv")

    output = {
        "summary": {
            "positive": int((sentiment["sentiment"] == "positive").sum()),
            "neutral": int((sentiment["sentiment"] == "neutral").sum()),
            "negative": int((sentiment["sentiment"] == "negative").sum()),
            "complaints": int(sentiment["has_complaint"].sum()),
            "total": len(sentiment),
        },
        "keywords": keywords.to_dict(orient="records"),
        "reviews": sentiment[[
            "clean_review",
            "rating",
            "sentiment",
            "has_complaint"
        ]].head(200).to_dict(orient="records")
    }

    with open(RESULTS_DIR / "dashboard.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("Exported dashboard.json")
