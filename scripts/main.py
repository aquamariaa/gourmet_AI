import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from scripts.pipeline.extract import extract
from scripts.pipeline.load import load
from scripts.pipeline.transform import transform
from scripts.analysis.analyze import analyze
from scripts.analysis.export import export_json


def main():
    print("🚀 Starting Gourmet AI Pipeline")

    extract()
    load()
    transform()
    analyze()

    print("✅ Pipeline completed successfully")


if __name__ == "__main__":
    main()
