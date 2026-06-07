"""
score.py 
-------------------------------

Job: Combine the Content Score (from content analysis) with the Repo Stats Score (from scorer.py) to produce a final overall score for each repo.
Input: scored repos from scorer.py, plus content scores from content analysis
Output: repos with final overall score and breakdown of how content and stats contributed
"""


def _score_overall(repo: dict) -> dict:
    """
    Combine the Repo Stats Score and the Content Score to produce an overall score.
    
    For simplicity, we can take a weighted average of the two scores. 
    The weights can be adjusted based on how much importance we want to give to content vs stats.
    
    Returns a dict with the overall score and breakdown of contributions.
    """
    stats_score   = repo.get("stats_score", 0.0)  # From scorer.py
    content_score = repo.get("content_score", 0.0)  # From content analysis
    
    # Define weights (these can be tuned)
    stats_weight   = 0.3
    content_weight = 0.7
    
    overall_score = round(stats_score * stats_weight + content_score * content_weight, 4)
    
    return {
        "overall_score": overall_score,
        "final_breakdown": {
            "stats_contribution": round(stats_score * stats_weight, 4),
            "content_contribution": round(content_score * content_weight, 4),
        }
    }