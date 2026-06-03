from src.Ingest_Layer.ingestion import ingest_data
from src.Github_Layer.orchestrator import orchestrate_github_search_with_stats
from src.Ranker.orchestrator import run_ranking_pipeline
from src.content_Analyzer.orchestrator import run_analysis_pipeline
from src.config import GITHUB_HEADER as headers

def main():
    data = ingest_data()
    if not data or data is None:
        return
    repos = orchestrate_github_search_with_stats(data)
    
    scored_repos = run_ranking_pipeline(repos.get("repositories", []))
    
    analyzed_repos = run_analysis_pipeline(scored_repos, headers)
    

if __name__ == "__main__":
    main()