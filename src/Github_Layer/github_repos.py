import requests
import time
from ..config import GITHUB_URL

def fetch_github_repos(query: str) -> dict:
    """
        Fetch GitHub repositories based on the provided query with pagination.
        Pagination is set to 100 repos per request, sorted by stars in descending order.
        
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
        'per_page': 100
    }
    
    start_time = time.perf_counter()
    
    response = requests.get(GITHUB_URL, headers=headers, params=params)
    
    elapsed = time.perf_counter() - start_time
    print(f"GitHub API request completed in {elapsed:.2f} seconds.")
    
    if response.status_code == 200:
        start = time.perf_counter()
        data =  response.json()
        parse_time = time.perf_counter() - start
        print(f"Data parsing completed in {parse_time:.2f} seconds.")
        print(f"Total count: {data['total_count']}")
        print(f"Returned repos: {len(data['items'])}")
        return data
    else:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")