"""
tree_fetcher.py
------------------------------
Fetch the content tree for a given repository using the GitHub API. This module provides functions to retrieve the file structure and content of a repository, which can be used for further analysis or processing.

Job: Fetch the content tree for a given repository using the GitHub API.
Input: Repository information (e.g., owner, repo name) and GitHub API headers for authentication.
Output: A structured representation of the repository's content tree, including file paths and their corresponding content
"""

from ..config import GITHUB_TREE_URL_TEMPLATE
import requests

def fetch_content_tree(repo: dict, headers: dict) -> dict:
    """
    Fetch the content tree for a given repository using the GitHub API.

    Parameters:
        repo (dict): A dictionary containing repository information (e.g., owner, repo name).
        headers (dict): Headers to include in the API request (e.g., for authentication).

    Returns:
        dict: A structured representation of the repository's content tree.
    """
    repo_name = repo.get('title')
    owner = repo.get('owner')
    
    if not repo_name or not owner:
        return {'file_structure': None}
    
    tree_url = GITHUB_TREE_URL_TEMPLATE.format(owner=owner, repo=repo_name, sha='HEAD')
    try:
        response = requests.get(tree_url, headers=headers)
        response.raise_for_status()
        
        if response.status_code == 200:
            tree_data = response.json()
            return {'file_structure': tree_data.get('tree', [])}
        else:
            return {'file_structure': None}
        
    except requests.RequestException:
        return {'file_structure': None}