"""
data_presenter.py
--------------------------------

Job: Present the Final Recommendations in a user-friendly format in the console.
Input: List of recommended repositories with their details.
Output: Printed details of recommended repositories in the console.
"""

def present_recommendations(recommended_repos):
    """
    Presents the recommended repositories in a user-friendly format in the console.
    
    Args:
        recommended_repos (list): List of recommended repositories with their details.
    """
    for repo in recommended_repos:
        print('=' * 50)
        print(f"Repository Name: {repo.get('title')}")
        print(f"URL: {repo.get('url')}")
        print(f"Description: {repo.get('description')}")
        if 'topics' in repo and len(repo['topics']) > 0:
            print(f"Topics: {', '.join(repo.get('topics', []))}")
        print(f"Score: {repo.get('overall_score')}")
        print(f"Reason for Recommendation: {repo.get('readme_analysis')}")
        print('=' * 50, "\n\n")