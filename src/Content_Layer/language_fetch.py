"""
language_fetch.py
------------------------------
Fetch the programming languages used in a given repository using the GitHub API. This module provides functions to retrieve the languages associated with a repository, which can be used for further analysis or processing.

Job: Fetch the programming languages used in a given repository using the GitHub API.
Input: Repository information (e.g., owner, repo name) and GitHub API headers
Output: A dictionary containing the programming languages used in the repository and their corresponding byte counts.
"""
import requests

def fetch_languages(repo:dict, headers: dict) -> dict:
    """
    Fetch the programming languages used in a given repository using the GitHub API.
    
    Parameters:
        repo (dict): A dictionary containing repository information (e.g., owner, repo name).
        headers (dict): Headers to include in the API request (e.g., for authentication).
        
    Returns:
        dict: A dictionary containing the programming languages used in the repository and their corresponding byte counts, or None if fetching fails.
    """
    
    languages_url = repo.get('languages_url')
    if not languages_url:
        return {'languages': None}
    
    try:
        response = requests.get(languages_url, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
<<<<<<< Updated upstream
            print(response.json())
=======
>>>>>>> Stashed changes
            return {'languages': response.json()}
        else:
            return {'languages': None}
        
    except requests.RequestException:
        return {'languages': None}