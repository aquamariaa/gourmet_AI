from ELT.ingest import ingest
from ELT.load import load
from ELT.transform import preprocess
from analysis.lightweight import analyze

def run_pipeline():
    print("🚀 Starting Gourmet AI Pipeline")

    print("▶ Step 1: Ingest")
    ingest()

    print("▶ Step 2: Load")
    load()

    print("▶ Step 3: Transform")
    preprocess()

    print("▶ Step 3: lightweight")
    analyze()

    print("✅ Pipeline completed successfully")

if __name__ == "__main__":
    run_pipeline()
