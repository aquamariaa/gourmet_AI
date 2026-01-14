from pathlib import Path
import pandas as pd

# ---------- PATHS ----------
RESULTS_DIR = Path("data/results")
DASHBOARD_DATA_DIR = Path("app/data")

DASHBOARD_DATA_DIR.mkdir(parents=True, exist_ok=True)

LIGHTWEIGHT_FILE = RESULTS_DIR / "lightweight_analysis.csv"
KEYWORD_FILE = RESULTS_DIR / "keyword_frequency.csv"


# ---------- BUILDERS ----------
def build_sentiment_summary(df: pd.DataFrame):
    summary = (
        df["sentiment"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "sentiment", "sentiment": "count"})
    )
    summary.to_csv(DASHBOARD_DATA_DIR / "sentiment_summary.csv", index=False)


def build_rating_distribution(df: pd.DataFrame):
    ratings = (
        df["rating"]
        .value_counts()
        .sort_index()
        .reset_index()
        .rename(columns={"index": "rating", "rating": "count"})
    )
    ratings.to_csv(DASHBOARD_DATA_DIR / "rating_distribution.csv", index=False)


def build_keywords():
    if KEYWORD_FILE.exists():
        pd.read_csv(KEYWORD_FILE).to_csv(
            DASHBOARD_DATA_DIR / "keyword_frequency.csv",
            index=False
        )

def build_reviews_table(df: pd.DataFrame):
    reviews = pd.DataFrame({
        "date": "",  # no date available from AI pipeline
        "rating": df["rating"],
        "sentiment": df["sentiment"],
        "review": df["clean_review"]
    })

    reviews.to_csv(
        DASHBOARD_DATA_DIR / "reviews.csv",
        index=False
    )

# ---------- ENTRY ----------
def prepare_dashboard():
    print("Preparing dashboard data...")

    if not LIGHTWEIGHT_FILE.exists():
        raise FileNotFoundError("lightweight_analysis.csv not found")

    df = pd.read_csv(LIGHTWEIGHT_FILE)

    build_sentiment_summary(df)
    build_rating_distribution(df)
    build_keywords()
    build_reviews_table(df)

    print("Dashboard data ready → app/data/")



if __name__ == "__main__":
    prepare_dashboard()
