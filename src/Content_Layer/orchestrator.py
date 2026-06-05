"""
orchestrator.py - Content Layer: Orchestrator
----------------------------------------------
Wires the full content fetching pipeline in sequence:

Job: For each repo, fetch README content and attach it to the repo dict for later analysis.
Input:  List of scored + ranked repo dicts from Ranker Layer (with 'contents_url' field)
Output: Same list with 'readme_content' field added (raw text or None)
"""

from .readme_fetch import fetch_readme_content
from .tree_fetcher import fetch_content_tree
from .language_fetch import fetch_languages

def fetch_content_for_single_repo(repo: dict, headers: dict) -> dict:
    """
    Fetch content for a single repo and attach it to the repo dict.

    Parameters:
        repo (dict): A repository dictionary containing at least the 'contents_url' field.
        headers (dict): Headers to include in the API request (e.g. for authentication).

    Returns:
        dict: The updated repository dictionary with 'readme_content' field added, or None if fetching fails.
    """
    readme_content = fetch_readme_content(repo, headers)
    file_struture = fetch_content_tree(repo, headers)
    languages = fetch_languages(repo, headers)
    
    repo['readme_content'] = readme_content.get('text') if readme_content else None
    repo['file_structure'] = file_struture.get('file_structure') if file_struture else None
    repo['languages'] = languages.get('languages') if languages else None
    
    return fetch_readme_content(repo, headers)

def fetch_content_for_repos(repos: list[dict], headers: dict) -> list[dict]:
    """
    Fetch content for a list of repos.

    Parameters:
        repos (list[dict]): A list of repository dictionaries.
        headers (dict): Headers to include in the API requests.

    Returns:
        list[dict]: The updated list of repository dictionaries with 'readme_content' field added.
    """
    for repo in repos:
        fetch_content_for_single_repo(repo, headers)
        
        
    return repos
