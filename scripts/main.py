import pipeline

def main():
    print("Initializing Wongnai AI Pipeline...")
    
    pipeline.extract_data()
    pipeline.transform_data()
    pipeline.analyze_and_load()
    
    print("\nPipeline finished successfully.")

if __name__ == "__main__":
    main()