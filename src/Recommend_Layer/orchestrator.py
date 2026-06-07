"""
orchestrator.py
-------------------------------

Job: Orchestrate the entire ranking pipeline by calling the individual steps in sequence.
Input: Top N repos with content fetched and analyzed, plus their stats from GitHub. 
Output: Top 3 recommended repos with final scores and breakdowns
"""

from .score import _score_overall
from .sorter import sort_repos_by_score

def run_recommend_ranking_pipeline(repos: list) -> list:
    """
    Orchestrate the ranking pipeline by calling the scoring and sorting functions in sequence.
    
    Steps:
    1. For each repo, calculate the overall score using _score_overall.
    2. Sort the repos by their overall score and return the top 3.
    
    Returns a list of the top 3 recommended repos with their scores and breakdowns.
    """
    # Step 1: Calculate overall score for each repo
    for repo in repos:
        score_info = _score_overall(repo)
        repo["overall_score"] = score_info["overall_score"]
        repo["final_score_breakdown"] = score_info["final_breakdown"]
    
    # Step 2: Sort repos by overall score and return top 3
    top_repos = sort_repos_by_score(repos)
    
    return top_repos