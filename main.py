import json

from src.Ingest_Layer.ingestion import ingest_data
from src.Github_Layer.orchestrator import orchestrate_github_search_with_stats
from src.Ranker.orchestrator import run_ranking_pipeline

from src.Content_Layer.orchestrator import fetch_content_for_repos

from src.Content_Layer.orchestrator import fetch_content_for_repos
from src.Analyzer.orchestrator import analyze_repository_content


from src.config import GITHUB_HEADER as headers

def main():
    
    
    data = ingest_data()
    if not data or data is None:
        return
    repos = orchestrate_github_search_with_stats(data)
    
    scored_repos = run_ranking_pipeline(repos.get("repositories", []))
    

    content_fetched = fetch_content_for_repos(scored_repos, headers)
    
    analyzed_repos = analyze_repository_content(content_fetched) 
    
    for repo in analyzed_repos:
        print(f"{repo['owner']}/{repo['title']}: {repo['content_score']:.2f}: Readme Score: {repo['readme_score']:.2f}, Tree Score: {repo['tree_score']:.2f} :: Score:{repo['score']} :: TOPICS: {', '.join(repo.get('topics', []))}", end="\n\n")   
    

if __name__ == "__main__":
    main()