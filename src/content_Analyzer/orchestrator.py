"""
orchestrator.py — Analyzer Layer
----------------------------------
Runs the full analysis pipeline for each repo in the top N list.
Makes at most 3 API calls per repo: README + structure + languages.

This is the only file the Reporter Layer imports from.

Input:  top N repo list from Ranker Layer
Output: same list with 'analysis' dict attached to each repo
"""

import requests
from .readme_reader     import read_readme
from .tree_extract      import extract_file_tree


def analyze_repo(repo: dict, headers: dict) -> dict:
    """
    Run full analysis on a single repo.
    Makes up to 3 API calls: README, root structure, languages.

    Returns:
        analysis dict containing readme, structure, complexity, and concepts data
    """
    title = repo.get("title", "unknown")

    readme_data = read_readme(repo, headers)       # call 1
    tree_data  = extract_file_tree(repo, headers) # call 2
   
    return {
        "readme":  readme_data,
        "tree":    tree_data
    }


def run_analysis_pipeline(repos: list[dict], headers: dict) -> list[dict]:
    """
    Analyze all repos in the top N list.
    Attaches 'analysis' key to each repo dict.

    Parameters:
        repos:   top N repo list from Ranker Layer
        headers: GitHub API auth headers

    Returns:
        same list with 'analysis' attached to each repo
    """
    total = len(repos)

    for i, repo in enumerate(repos, start=1):
        repo["analysis"] = analyze_repo(repo, headers)
        
    print(repos[0])

    return repos