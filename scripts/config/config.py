from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

RAW_DIR = DATA_DIR / "raw"
STAGED_DIR = DATA_DIR / "staged"
RESULTS_DIR = DATA_DIR / "results"

RAW_FILE = RAW_DIR / "raw_reviews.csv"
STAGED_FILE = STAGED_DIR / "reviews_loaded.csv"
CLEAN_FILE = RESULTS_DIR / "reviews_clean.csv"

ANALYSIS_FILE = RESULTS_DIR / "lightweight_analysis.csv"
KEYWORD_FILE = RESULTS_DIR / "keyword_frequency.csv"
