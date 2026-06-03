"""
orchestrator.py — Ranker Layer: Orchestrator
----------------------------------------------
Wires the full ranking pipeline in sequence:
    gate → scorer → ranker → selector

This is the only file the layer above (Analyzer) imports from.
Internal files (gate, scorer, ranker, selector) are not exposed outside.

Input:  raw repo list from GitHub Layer
Output: top N scored + ranked repo dicts
"""

from .validate_weight import run_all as validate
from .gate             import apply_gates
from .scorer           import score_repos
from .ranker           import rank_repos
from .selector         import select_top_n


def run_ranking_pipeline(repos: list[dict], top_n: int | None = None) -> list[dict]:
    """
    Execute the full ranking pipeline.

    Parameters:
        repos: raw repo dicts from GitHub Layer
        top_n: how many repos to return (None = use selector default)

    Returns:
        top N repos with score, score_breakdown, rank, and pushed_at attached
    """

    print(f"\n{'='*60}")
    print(f"[ranker_orchestrator] Pipeline start — {len(repos)} repos received")
    print(f"{'='*60}")

    # Pass 1 — Gate
    passed_repos, dropped_repos = apply_gates(repos)

    if not passed_repos:
        print("[orchestrator] No repos passed gating. Returning empty list.")
        return []

    # Pass 2 — Score
    scored_repos = score_repos(passed_repos)

    # Pass 3 — Rank
    ranked_repos = rank_repos(scored_repos)

    # Pass 4 — Select
    top_repos = select_top_n(ranked_repos, n=top_n)

    print(f"\n{'='*60}")
    print(f"[ranker_orchestrator] Done — returning {len(top_repos)} repos")
    print(f"{'='*60}\n")

    return top_repos