import json

from src.Ingest_Layer.ingestion import ingest_data
from src.Github_Layer.orchestrator import orchestrate_github_search_with_stats
from src.Ranker.orchestrator import run_ranking_pipeline

from src.Content_Layer.orchestrator import fetch_content_for_repos

from src.Content_Layer.orchestrator import fetch_content_for_repos

from src.Content_Layer.orchestrator import fetch_content_for_repos
from src.Analyzer.orchestrator import analyze_repository_content

from src.Recommend_Layer.orchestrator import run_recommend_ranking_pipeline

from src.Report.data_presenter import present_recommendations

from src.config import GITHUB_HEADER as headers

def main():
    
    
    data = ingest_data()
    if not data or data is None:
        return
    repos = orchestrate_github_search_with_stats(data)
    
    scored_repos = run_ranking_pipeline(repos.get("repositories", []))

    content_fetched = fetch_content_for_repos(scored_repos, headers)
    
    analyzed_repos = analyze_repository_content(content_fetched) 
    
    final_recommendations_repos = run_recommend_ranking_pipeline(analyzed_repos)
    
    present_recommendations(final_recommendations_repos)


if __name__ == "__main__":
    main()