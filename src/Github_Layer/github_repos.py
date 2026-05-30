import requests
from ..config import GITHUB_URL

def fetch_github_repos(query: str) -> dict:
    """
        Fetch GitHub repositories based on the provided query with pagination.
        Pagination is set to 10 repos per request, sorted by stars in descending order.
        
        Parameters:
            query (str): A GitHub query string
            
        Returns:
            dict: A dictionary containing the fetched repositories
    """
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    
    params = {
        'q': query,
        'sort': 'stars',
        'order': 'desc',
        'per_page': 10
    }
    
    response = requests.get(GITHUB_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")