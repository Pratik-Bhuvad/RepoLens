from src.Ingest_Layer.ingestion import ingest_data
from src.Github_Layer.orchestrator import orchestrate_github_search_with_stats

def main():
    data = ingest_data()
    if not data or data is None:
        return
    repos = orchestrate_github_search_with_stats(data)
    
    print("Extracted Repositories:" ,repos)

if __name__ == "__main__":
    main()