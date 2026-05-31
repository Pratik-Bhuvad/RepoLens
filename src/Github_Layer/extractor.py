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
                'title': repo.get('name'),
                'description': repo.get('description'),
                'url': repo.get('html_url'),
                'topics': repo.get('topics', []),
                'languages': repo.get('language'),
                'languages_url': repo.get('languages_url'),
                'contributors_url': repo.get('contributors_url'),
                'contents_url': repo.get('contents_url'),
                'deployment': repo.get('deployments_url', None),  # Assuming 'deployment' is a field in the API response
                'license': repo.get('license', {}).get('name') if repo.get('license') else None
            }
            extracted_repos.append(extracted_data)
        except (KeyError, TypeError, AttributeError) as e:
            # Skip repositories with extraction errors, continue with next repo
            continue
    
    return extracted_repos
