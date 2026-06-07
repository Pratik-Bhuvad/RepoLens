"""
sorter.py
-------------------------------

Job: Sort the scored repos based on their overall score and return the top 3 repos.
Input: scored repos with overall scores from score.py
Output: top 3 repos sorted by overall score
"""

def sort_repos_by_score(repos: list) -> list:
    """
    Sort the repos based on their overall score in descending order and return the top 3.
    """
    sorted_repos = sorted(repos, key=lambda r: r.get("overall_score", 0.0), reverse=True)
    return sorted_repos[:3]