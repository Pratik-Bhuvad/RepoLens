"""
scorer.py — Ranker Layer: Scorer
----------------------------------
Second pass. Calculates a 0.0-1.0 score for each repo that passed gate.py.
fork_star_ratio is computed here from raw stars + forks — not pre-calculated.

Job: attach score + breakdown to each repo. Nothing else.
Input:  passed_repos from gate.py
Output: same list with 'score' and 'score_breakdown' added
"""

import math
from .weights import SCORE_WEIGHTS


# ---------------------------------------------------------------------------
# Per-field scoring functions — each returns float 0.0-1.0
# ---------------------------------------------------------------------------

def _score_fork_star_ratio(repo: dict, config: dict) -> float:
    """
    Computed from raw stars + forks.
    LOW ratio (more stars than forks) = real project signal → high score.

    Edge cases:
        - stars=1, forks=1 → both below threshold → neutral 0.5
        - forks=0 → no signal either way → neutral 0.5
        - ratio > 1 (more forks than stars) → strong tutorial signal → low score
    """
    stars = repo.get("stars", 0)
    forks = repo.get("forks", 0)

    min_stars = config.get("min_stars_threshold", 15)
    min_forks = config.get("min_forks_threshold", 3)

    # Not enough data — return neutral
    if stars < min_stars or forks < min_forks:
        return 0.5

    ratio = forks / stars                # e.g. 166/358 = 0.46
    ratio_clamped = min(ratio, 1.0)      # cap at 1.0 — beyond that it's max tutorial signal
    return round(1.0 - ratio_clamped, 4) # invert — low ratio → high score


def _score_open_issues(repo: dict, config: dict) -> float:
    """
    1-cap issues = real project signal. 0 = neutral. Beyond cap = no extra benefit.
    """
    issues = repo.get("open_issues", 0)
    cap    = config.get("score_cap", 20)

    if issues == 0:
        return 0.0   # Neutral — no bonus, no penalty

    return round(min(issues / cap, 1.0), 4)


def _score_description_signal(repo: dict, config: dict) -> float:
    """
    Scans description for project / tutorial / boilerplate language.

    Scoring:
        - project word found     → +0.2 per word, capped at 1.0
        - tutorial word found    → -0.4 per word, floored at 0.0
        - boilerplate word found → -0.3 per word, floored at 0.0
        - no description         → neutral 0.5
        - no signal words found  → neutral 0.5
    """
    description = repo.get("description") or ""

    if not description.strip():
        return 0.5

    desc_lower = description.lower()

    project_words     = config.get("project_words", [])
    tutorial_words    = config.get("tutorial_words", [])
    boilerplate_words = config.get("boilerplate_words", [])

    score = 0.5  # Start neutral

    for word in project_words:
        if word in desc_lower:
            score += 0.2

    for word in tutorial_words:
        if word in desc_lower:
            score -= 0.4

    for word in boilerplate_words:
        if word in desc_lower:
            score -= 0.3

    return round(max(0.0, min(score, 1.0)), 4)  # Clamp to [0.0, 1.0]


def _score_forks(repo: dict, config: dict) -> float:
    """
    Log-scaled raw fork count. Diminishing returns above log_ceiling.
    math.log1p(0) = 0.0 — zero forks handled correctly with no guard needed.
    """
    forks       = repo.get("forks", 0)
    log_ceiling = config.get("log_ceiling", 100)

    return round(min(math.log1p(forks) / math.log1p(log_ceiling), 1.0), 4)


def _score_license(repo: dict, config: dict) -> float:
    """
    Binary + preferred license bonus.
    No license → 0.0 (neutral). Any license → 0.5. Preferred license → 1.0.
    """
    license_name = repo.get("license")

    if not license_name:
        return 0.0

    preferred = config.get("preferred_licenses", [])
    return 1.0 if license_name in preferred else 0.5


def _score_has_topics(repo: dict, config: dict) -> float:
    """Binary. Has topics → 1.0. No topics → 0.0."""
    topics = repo.get("topics", [])
    return 1.0 if topics else 0.0


def _is_boilerplate_repo(repo: dict, config: dict) -> bool:
    """
    Detect if repo is a boilerplate/starter/template repo.
    Returns True if boilerplate is detected — these repos will be discarded.
    
    Checks:
        - Description contains boilerplate words
        - Topics tagged as boilerplate
    """
    description = repo.get("description") or ""
    desc_lower = description.lower()
    
    boilerplate_words = config.get("boilerplate_words", [])
    
    # Check description for boilerplate language
    for word in boilerplate_words:
        if word in desc_lower:
            return True
    
    # Check topics for boilerplate tags
    topics = repo.get("topics", [])
    for topic in topics:
        if topic.lower() in boilerplate_words:
            return True
    
    return False


# ---------------------------------------------------------------------------
# Dispatch — field name → scoring function
# ---------------------------------------------------------------------------

FIELD_SCORERS = {
    "fork_star_ratio":    _score_fork_star_ratio,
    "open_issues":        _score_open_issues,
    "description_signal": _score_description_signal,
    "forks":              _score_forks,
    "license":            _score_license,
    "has_topics":         _score_has_topics,
}


# ---------------------------------------------------------------------------
# Main scorer
# ---------------------------------------------------------------------------

def score_repos(repos: list[dict]) -> list[dict]:
    """
    Score each repo. Adds 'score' and 'score_breakdown' to every repo dict.
    
    Boilerplate repos (detected via description or topics) are completely
    discarded and do NOT appear in the output.

    Parameters:
        repos: gated list from gate.py

    Returns:
        scored list (excluding all boilerplate repos) with score fields attached
    """
    boilerplate_config = SCORE_WEIGHTS.get("description_signal", {})
    
    # Filter out boilerplate repos completely
    filtered_repos = []
    for repo in repos:
        if _is_boilerplate_repo(repo, boilerplate_config):
            continue  # Discard boilerplate repos entirely
        filtered_repos.append(repo)
    
    # Score remaining repos
    for repo in filtered_repos:
        total_score = 0.0
        breakdown   = {}

        for field, config in SCORE_WEIGHTS.items():
            if not config.get("enabled", True):
                continue

            scorer_fn = FIELD_SCORERS.get(field)
            if scorer_fn is None:
                continue

            raw          = scorer_fn(repo, config)     # 0.0 – 1.0
            
            weight       = config["weight"]
            contribution = round(raw * weight, 4)

            breakdown[field] = {
                "raw":          raw,
                "weight":       weight,
                "contribution": contribution,
            }

            total_score += contribution

        repo["stats_score"]           = round(total_score, 4)
        repo["stats_score_breakdown"] = breakdown

    return filtered_repos