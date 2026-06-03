"""
selector.py — Ranker Layer: Selector
--------------------------------------
Fourth pass. Returns top N repos from the ranked list.

Job: slice. Nothing else.
Input:  ranked list from ranker.py
Output: top N repos
"""

from .weights import SELECTOR_CONFIG


def select_top_n(repos: list[dict], n: int | None = None) -> list[dict]:
    """
    Return top N repos from a ranked list.
    Uses default_top_n from weights.SELECTOR_CONFIG if n not provided.
    Returns all repos if fewer than N exist — never errors on small sets.

    Parameters:
        repos: ranked list from ranker.py
        n:     how many repos to return (None = use config default)

    Returns:
        top N repo dicts
    """
    top_n = n if n is not None else SELECTOR_CONFIG.get("default_top_n", 5)

    if not repos:
        print("[selector] No repos to select from.")
        return []

    if top_n <= 0:
        print(f"[selector] Invalid n={top_n}. Must be > 0.")
        return []

    selected = repos[:top_n]
    total    = len(repos)

    print(f"\n[selector] Selected top {len(selected)} from {total} ranked repos")

    if total < top_n:
        print(f"  Note: requested {top_n} but only {total} available after gating + scoring")

    return selected