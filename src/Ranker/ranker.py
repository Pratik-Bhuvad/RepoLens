"""
ranker.py — Ranker Layer: Ranker
----------------------------------
Third pass. Sorts scored repos.

Primary sort:   score (descending)
Secondary sort: pushed_at date (descending) — recency breaks ties between close scores

"Close" is defined by score_proximity_threshold in weights.RANKING_CONFIG.
Two repos within that threshold are considered tied → pushed_at decides.

Job: sort + attach rank. Nothing else.
Input:  scored list from scorer.py
Output: same list sorted, with 'rank' field added
"""

from datetime import datetime
from .weights  import RANKING_CONFIG


def _parse_date(date_str: str | None) -> datetime:
    """
    Parse ISO date string to datetime for comparison.
    Falls back to epoch (1970-01-01) if missing or malformed — 
    ensures repos with no date sink to the bottom on tiebreaks.
    """
    if not date_str:
        return datetime.min

    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    return datetime.min


def _sort_key(repo: dict, threshold: float):
    """
    Sort key for two-pass ranking.

    Primary:   score bucket — score floored to nearest threshold step
               Repos within the same bucket are "tied"
    Secondary: pushed_at date — most recent wins within a bucket

    Example with threshold=0.05:
        score=0.73 → bucket=14  (0.73 // 0.05)
        score=0.71 → bucket=14  (tied → recency decides)
        score=0.68 → bucket=13  (genuinely lower ranked)
    """
    score      = repo.get("score", 0.0)
    pushed_at  = _parse_date(repo.get("pushed_at"))
    score_bucket = int(score // threshold)

    # Return as negatives because sorted() is ascending by default
    return (-score_bucket, -pushed_at.timestamp())


def rank_repos(repos: list[dict]) -> list[dict]:
    """
    Sort repos by score (primary) + pushed_at (secondary tiebreaker).
    Attach 1-based rank to each repo.

    Parameters:
        repos: scored list from scorer.py

    Returns:
        sorted list with 'rank' attached
    """
    if not repos:
        print("[ranker] No repos to rank.")
        return []

    threshold = RANKING_CONFIG.get("score_proximity_threshold", 0.05)

    ranked = sorted(repos, key=lambda r: _sort_key(r, threshold))

    for position, repo in enumerate(ranked, start=1):
        repo["rank"] = position

    return ranked