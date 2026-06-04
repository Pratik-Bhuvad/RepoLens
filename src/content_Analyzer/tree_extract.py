"""
tree_extract.py — Analyzer Layer
-----------------------------------

Job: Extract file tree structure for each repo. Nothing else.
Input:  single repo dict (must have contents_url)
Output: dict with 'file_tree' key containing list of file paths, or None if unavailable

"""

from ..config import GITHUB_TREE_URL_TEMPLATE, GITHUB_HEADER as headers
import requests

def extract_file_tree(repo: dict, headers: dict) -> dict:
    """
    Fetch and extract the file tree structure for a repo.

    Parameters:
        repo:    dict containing at least 'full_name' key (format: "owner/repo")
        headers: GitHub API auth headers
        
    Returns:
        dict with 'file_tree' key containing list of file paths, or None if not found
    """
    
    repo_name = repo.get("title", "")
    repo_owner = repo.get("owner", "")
    if not repo_name or not repo_owner:
        return {"file_tree": None}
    
    # Step 1: Get the default branch's latest commit SHA
    tree_url = GITHUB_TREE_URL_TEMPLATE.format(owner=repo_owner, repo=repo_name, sha="HEAD")
    response = requests.get(tree_url, headers=headers)
    
    if response.status_code != 200:
        print(f"  [tree_extract] No file tree found for '{repo.get('title')}'")
        return {"file_tree": None}
    if response.status_code == 403:
        print(f"[tree_extract] Rate limit hit when fetching file tree for '{repo.get('title')}'")
        return {"file_tree": None}
    
    tree_data = response.json()
    if "tree" not in tree_data:
        return {"file_tree": None}
    
    return tree_data.get("tree", [])