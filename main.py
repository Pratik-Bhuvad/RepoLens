from src.Ingest_Layer.ingestion import ingest_data
from src.Github_Layer.github_orchestrator import orchestrate_github_search

def main():
    data = ingest_data()
    if not data or data is None:
        return
    repos = orchestrate_github_search(data)
    
    print("Extracted Repositories:" ,repos)

if __name__ == "__main__":
    main()