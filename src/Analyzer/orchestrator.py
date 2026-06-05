"""
Orchestrator module for Analyzing Content of Codebase
"""
from .understandbility import analyze_repositories_understandability
from .educational_value import analyze_repositories_educational_value

def analyze_repository_content(repos: list[dict]) -> list[dict]:
    """
    Orchestrates the analysis of repository content by calling various analysis functions.
    
    Args:
        repos: List of repository dictionaries to analyze
    
    Returns:
        List of repositories with added analysis results
    """
    # Import analysis functions here to avoid circular imports
    
    # Step 1: Analyze understandability for all repositories
    repos = analyze_repositories_understandability(repos)
    
    # Step 2: Analyze educational value for all repositories
    repos = analyze_repositories_educational_value(repos)
    
    return repos
    