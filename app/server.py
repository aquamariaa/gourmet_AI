from flask import Flask, render_template, jsonify
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "results"

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/sentiment")
def sentiment():
    df = pd.read_csv(DATA_DIR / "lightweight_analysis.csv")
    counts = df["sentiment"].value_counts().to_dict()
    return jsonify(counts)

@app.route("/api/keywords")
def keywords():
    df = pd.read_csv(DATA_DIR / "keyword_frequency.csv")
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
