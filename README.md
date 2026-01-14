# Gourmet AI

## Overview

Gourmet AI is an end-to-end data pipeline designed to analyze restaurant customer reviews and extract actionable business insights. The system ingests large-scale public review data, cleans and preprocesses unstructured Thai text, performs lightweight sentiment analysis and keyword-based issue detection, and produces structured outputs suitable for reporting and decision-making.

This project is designed with academic clarity and engineering discipline in mind: reproducible runs, modular architecture, and clearly defined pipeline stages.

---

## Project Objectives

- Collect restaurant review data at scale
- Clean and normalize noisy, real-world text data
- Perform rule-based sentiment analysis optimized for short reviews
- Extract business-relevant keywords and complaints
- Generate structured outputs for further reporting and analysis

---

## System Architecture

```
Raw Reviews
     │
     ▼
[ Ingestion ]  →  data/raw/raw_reviews.csv
     │
     ▼
[ Preprocessing ]  →  data/results/reviews_clean.csv
     │
     ▼
[ Analysis ]  →  lightweight_analysis.csv
                keyword_frequency.csv
```

Each stage is isolated, reproducible, and independently testable.

---

## Project Structure

```
.
├── analysis/
│   └── lightweight.py        # Lightweight sentiment & keyword analysis
├── app/
│   ├── main.py               # Application entry point
│   └── pipeline.py           # Orchestrates the full pipeline
├── config/
│   └── settings.py           # Global paths & constants
├── data/
│   ├── raw/                  # Raw ingested data
│   ├── staged/               # Intermediate cleaned data
│   └── results/              # Final analysis outputs
├── ingestion/
│   └── wongnai.py             # Dataset ingestion logic
├── preprocessing/
│   └── clean_reviews.py      # Text cleaning & normalization
├── venv/                     # Python virtual environment
├── requirements.txt
├── Makefile
└── README.md
```

---

## Pipeline Stages

### 1. Ingestion

- Source: Wongnai restaurant review dataset
- Output: `data/raw/raw_reviews.csv`
- Responsibility: dataset download and raw storage

### 2. Preprocessing

- Text normalization
- Noise and symbol removal
- Review splitting (multi-review entries)
- Output: `data/results/reviews_clean.csv`

### 3. Analysis (Lightweight)

- Rule-based sentiment classification
- Complaint detection
- Business keyword frequency extraction
- Outputs:

  - `lightweight_analysis.csv`
  - `keyword_frequency.csv`

---

## Lightweight Sentiment Logic

The lightweight analyzer is optimized for:

- Very short reviews
- Missing or unreliable ratings
- Thai-language complaint patterns

Sentiment decisions are based on:

- Review length
- Presence of strong / weak negative keywords
- Star rating (when available)

This approach prioritizes **robustness and interpretability** over black-box accuracy.

---

## Installation

### 1. Create virtual environment

```bash
make setup
```

### 2. Activate environment

```bash
source venv/bin/activate
```

---

## Running the Pipeline

### Run full pipeline

```bash
make run
```

### Run individual stages

```bash
make ingest
make preprocess
make analyze
```

---

## Outputs

| File                     | Description                    |
| ------------------------ | ------------------------------ |
| raw_reviews.csv          | Original dataset               |
| reviews_clean.csv        | Cleaned and normalized reviews |
| lightweight_analysis.csv | Sentiment & complaint labels   |
| keyword_frequency.csv    | Business keyword counts        |

---

## Design Principles

- Modular pipeline architecture
- Deterministic, reproducible runs
- Clear separation of concerns
- Minimal external dependencies
- Explainable analysis logic

---

## Limitations

- Rule-based sentiment analysis may miss nuanced context
- No sarcasm or implicit sentiment detection
- Dataset-specific keyword assumptions

These limitations are intentional trade-offs for interpretability and stability.

---

## Future Work

- Aspect-based sentiment analysis
- LLM-assisted review summarization
- Time-series trend analysis
- Automated weekly report generation

---

## Academic Context

This project is suitable for:

- Data engineering coursework
- Applied NLP projects
- Business intelligence system demonstrations

It emphasizes **pipeline correctness and analytical clarity** over model complexity.

---

## Contributors

Arocha Phuengthai

Sorawit Klaokliang

Chawaphon Duangploy

---

## License

For academic and educational use only.
