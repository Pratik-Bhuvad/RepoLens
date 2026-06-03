import json

def extract_repo_data(repos_response: dict) -> list:
    """
        Extract specific repository fields from GitHub API response.
        Handles None exceptions for missing fields.
        
        Parameters:
            repos_response (dict): The response dictionary from fetch_github_repos()
            
        Returns:
            list: A list of dictionaries containing extracted repository data with fields:
                  - title, description, languages, languages_url, contributors_url, contents_url
    """
    extracted_repos = []
    
    if 'items' not in repos_response or len(repos_response['items']) == 0:
        return extracted_repos
    

    for repo in repos_response['items']:
        try:
            extracted_data = {
                # Identity
                'title': repo.get('name'),
                'description': repo.get('description'),
                'url': repo.get('html_url'),
                'owner': repo.get('owner', {}).get('login'),
                'owner_type': repo.get('owner', {}).get('type'),  # "User" vs "Organization"
                'pushed_at': repo.get('pushed_at'),

                # Content signals
                'topics': repo.get('topics', []),
                'language': repo.get('language'),
                'license': repo.get('license', {}).get('name') if repo.get('license') else None,
                'size_kb': repo.get('size'),

                # Engagement signals (raw numbers — needed for scoring)
                'stars': repo.get('stargazers_count', 0),
                'forks': repo.get('forks_count', 0),
                'open_issues': repo.get('open_issues_count', 0),
                'watchers': repo.get('watchers_count', 0),

                # Computed score (derived from raw numbers above)
                'fork_star_ratio': round(
                    repo.get('forks_count', 0) / repo.get('stargazers_count', 1), 3
                ) if repo.get('stargazers_count', 0) > 0 else None,

                # URLs for future calls (Phase 2/3)
                'languages_url': repo.get('languages_url'),
                'contributors_url': repo.get('contributors_url'),
                'contents_url': repo.get('contents_url'),
            }
            extracted_repos.append(extracted_data)
        except (KeyError, TypeError, AttributeError) as e:
            # Skip repositories with extraction errors, continue with next repo
            continue
    
    return extracted_repos
