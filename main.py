from src.ingestion import ingest_data

def main():
    data = ingest_data()
    if data:
        print("Data ingested successfully:")
        print(data)
    
if __name__ == "__main__":
    main()