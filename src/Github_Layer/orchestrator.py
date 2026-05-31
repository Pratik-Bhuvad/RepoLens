"""
GitHub Layer Orchestrator
Coordinates the GitHub data fetching and processing workflow:
1. Build optimized GitHub query
2. Fetch repositories from GitHub API (with pagination)
3. Extract relevant repository data
"""

from .query_builder import build_github_query
from .fetcher import fetch_github_repos
from .extractor import extract_repo_data


def orchestrate_github_search(search_params: dict) -> list:
    """
        Orchestrate the complete GitHub search and extraction workflow.
        Fetches ALL repositories across all pages, not just page 1.
        
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
        
        # Step 2: Fetch all repositories from GitHub API (with pagination)
        all_extracted_repos = []
        per_page = 100
        page = 1
        
        # GitHub API has a limit of 1000 results per search (max 10 pages with per_page=100)
        max_pages = 10
        
        while page <= max_pages:
            repos_response = fetch_github_repos(github_query, page=page, per_page=per_page)
            
            # Check if we got any results
            if not repos_response.get('items'):
                break
            
            # Step 3: Extract relevant data from response
            extracted_repos = extract_repo_data(repos_response)
            all_extracted_repos.extend(extracted_repos)
            
            # If we have fewer items than per_page, we've reached the last page
            if len(repos_response.get('items', [])) < per_page:
                break
            
            page += 1
        
        return all_extracted_repos
        
    except Exception as e:
        raise Exception(f"GitHub search orchestration failed: {str(e)}")


def orchestrate_github_search_with_stats(search_params: dict) -> dict:
    """
        Orchestrate GitHub search with additional statistics.
        Fetches ALL repositories across all pages, not just page 1.
        
        Parameters:
            search_params (dict): Dictionary containing search parameters
            
        Returns:
            dict: Dictionary containing:
                - repositories (list): Extracted repository data
                - total_count (int): Total repositories found
                - query_used (str): The query string sent to GitHub API
                - pages_fetched (int): Number of pages fetched
                
        Raises:
            Exception: If GitHub API request fails
    """
    try:
        
        query = search_params.get('query', '')
        
        stack_qualifiers, concept_tokens = classify_query_stack(query)
        search_params['stack_qualifiers'] = stack_qualifiers
        search_params['concept_tokens'] = concept_tokens

        # Step 1: Build optimized query
        github_query = build_github_query(search_params)
        
        # Step 2: Fetch all repositories from GitHub API (with pagination)
        all_extracted_repos = []
        per_page = 100
        page = 1
        total_count = 0
        
        # GitHub API has a limit of 1000 results per search (max 10 pages with per_page=100)
        max_pages = 10
        
        while page <= max_pages:
            repos_response = fetch_github_repos(github_query, page=page, per_page=per_page)
            
            # Capture total count from first response
            if page == 1:
                total_count = repos_response.get('total_count', 0)
            
            # Check if we got any results
            if not repos_response.get('items'):
                break
            
            # Step 3: Extract relevant data from response
            extracted_repos = extract_repo_data(repos_response)
            all_extracted_repos.extend(extracted_repos)
            
            # If we have fewer items than per_page, we've reached the last page
            if len(repos_response.get('items', [])) < per_page:
                break
            
            page += 1
        
        # Compile results with statistics
        result = {
            'total_count': total_count,
            'query_used': github_query,
            'pages_fetched': page,
            'repos_fetched': len(all_extracted_repos),
            'repositories': all_extracted_repos,
        }
        
        return result
        
    except Exception as e:
        raise Exception(f"GitHub search orchestration with stats failed: {str(e)}")
