import json

from src.Ingest_Layer.ingestion import ingest_data
from src.Github_Layer.orchestrator import orchestrate_github_search_with_stats
from src.Ranker.orchestrator import run_ranking_pipeline
from src.Content_Layer.orchestrator import fetch_content_for_repos
from src.config import GITHUB_HEADER as headers

def main():
    data = ingest_data()
    if not data or data is None:
        return
    repos = orchestrate_github_search_with_stats(data)
    
    scored_repos = run_ranking_pipeline(repos.get("repositories", []))
    
    analyzed_repos = fetch_content_for_repos(scored_repos, headers)
    
    for repo in analyzed_repos:
        with open(f"sample_output/content_fetched/{repo['title']}.txt", "w", encoding="utf-8") as f:
            f.write(str(repo))

if __name__ == "__main__":
    main()