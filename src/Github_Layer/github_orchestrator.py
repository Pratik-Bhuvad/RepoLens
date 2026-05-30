"""
GitHub Layer Orchestrator
Coordinates the GitHub data fetching and processing workflow:
1. Build optimized GitHub query
2. Fetch repositories from GitHub API
3. Extract relevant repository data
"""

from .github_query_builder import build_github_query
from .github_repos import fetch_github_repos
from .github_extractor import extract_repo_data


def orchestrate_github_search(search_params: dict) -> list:
    """
        Orchestrate the complete GitHub search and extraction workflow.
        
        Parameters:
            search_params (dict): Dictionary containing search parameters:
                - language (str): Programming language filter
                - min_stars (int, optional): Minimum stars threshold
                - max_stars (int, optional): Maximum stars threshold
                - last_updated (str, optional): Date filter for last push
            
        Returns:
            list: List of extracted repository data dictionaries containing:
                  - title, description, languages, languages_url, 
                    contributors_url, contents_url
                    
        Raises:
            Exception: If GitHub API request fails
    """
    try:
        # Step 1: Build optimized query
        github_query = build_github_query(search_params)
        
        # Step 2: Fetch repositories from GitHub API
        repos_response = fetch_github_repos(github_query)
        
        # Step 3: Extract relevant data from response
        extracted_repos = extract_repo_data(repos_response)
        
        return extracted_repos
        
    except Exception as e:
        raise Exception(f"GitHub search orchestration failed: {str(e)}")


def orchestrate_github_search_with_stats(search_params: dict) -> dict:
    """
        Orchestrate GitHub search with additional statistics.
        
        Parameters:
            search_params (dict): Dictionary containing search parameters
            
        Returns:
            dict: Dictionary containing:
                - repositories (list): Extracted repository data
                - total_count (int): Total repositories found
                - query_used (str): The query string sent to GitHub API
                
        Raises:
            Exception: If GitHub API request fails
    """
    try:
        # Step 1: Build optimized query
        github_query = build_github_query(search_params)
        
        # Step 2: Fetch repositories from GitHub API
        repos_response = fetch_github_repos(github_query)
        
        # Step 3: Extract relevant data from response
        extracted_repos = extract_repo_data(repos_response)
        
        # Compile results with statistics
        result = {
            'repositories': extracted_repos,
            'total_count': repos_response.get('total_count', 0),
            'query_used': github_query,
            'repos_fetched': len(extracted_repos)
        }
        
        return result
        
    except Exception as e:
        raise Exception(f"GitHub search orchestration with stats failed: {str(e)}")
