"""
weights.py — Ranker Layer: Weight Configuration
-------------------------------------------------
Single source of truth for all scoring constants.
Nothing is computed here — only configured.

Rules:
    - All SCORE_WEIGHTS entries must sum to 1.0 (validated by validate_weights.py)
    - Gates are applied BEFORE scoring — failed repos never reach the scorer
    - Increase a weight to make that signal matter more in the final rank
"""

# ---------------------------------------------------------------------------
# GATES — Hard filters. Repos outside these bounds are dropped before scoring.
# Gates do NOT contribute to score — they only decide if a repo is evaluated.
# ---------------------------------------------------------------------------

GATES = {
    "stars": {
        "enabled":  True,
        "gate_min": 10,
        "gate_max": 500,
        "description": (
            "Min=10 filters spam/invisible repos. "
            "Max=500 avoids over-famous repos. "
            "Stars are NOT scored — scoring stars rewards tutorial creators with large audiences."
        ),
    },
    "size_kb": {
        "enabled":  True,
        "gate_min": 50,
        "gate_max": 50_000,
        "description": (
            "Min=50 filters empty skeletons. "
            "Max=50000 filters repos too large to navigate as a learner."
        ),
    },
}


# ---------------------------------------------------------------------------
# SCORE WEIGHTS — Weighted signals. Must sum to 1.0.
# ---------------------------------------------------------------------------

SCORE_WEIGHTS = {

    "fork_star_ratio": {
        "weight":  0.30,
        "enabled": True,
        "description": (
            "Core tutorial detector. "
            "Tutorial repos get forked heavily by students following along. "
            "Real projects get starred more than forked. "
            "LOW ratio = more stars per fork = real project signal. "
            "Computed in scorer from raw stars + forks fields."
        ),
        # Minimum thresholds before ratio is statistically meaningful
        # stars=1 forks=1 should NOT give 100% — both must clear floor
        "min_stars_threshold": 15,
        "min_forks_threshold": 3,
    },

    "open_issues": {
        "weight":   0.25,
        "enabled":  True,
        "description": (
            "Real projects have issues filed — real people used them and hit problems. "
            "Tutorials rarely have issues. Sweet spot: 1–20. "
            "Cap prevents broken/abandoned repos from scoring high."
        ),
        "score_cap":    20,    # Issues beyond this add no more score
        "zero_penalty": False, # 0 issues = neutral, not penalised
    },

    "description_signal": {
        "weight":  0.20,
        "enabled": True,
        "description": (
            "Scans description text for project vs tutorial vs boilerplate language. "
            "Project words = positive. Tutorial/boilerplate words = negative. "
            "No description = neutral 0.5."
        ),
        "project_words": [
            "made using", "built with", "app", "platform",
            "system", "tool", "manager", "tracker", "dashboard",
            "marketplace", "portal", "fullstack", "full-stack",
        ],
        "tutorial_words": [
            "tutorial", "course", "learn how", "guide", "follow along",
            "step by step", "beginner", "crash course", "series",
        ],
        "boilerplate_words": [
            "boilerplate", "starter", "template", "scaffold",
            "skeleton", "demo", "example", "sample",
        ],
    },

    "forks": {
        "weight":  0.15,
        "enabled": True,
        "description": (
            "Raw fork count — secondary engagement signal. "
            "Log-scaled to apply diminishing returns. "
            "Used alongside fork_star_ratio, not instead of it."
        ),
        "scale":       "log",
        "log_ceiling": 100,    # log(100) used as normalization ceiling
    },

    "license": {
        "weight":  0.05,
        "enabled": True,
        "description": (
            "A developer who added a license was thinking about others using their code. "
            "Builder mindset signal. Absence = neutral. Presence = small bonus."
        ),
        "bonus_if_present": True,
        "preferred_licenses": [
            "MIT License",
            "Apache License 2.0",
            "GNU General Public License v3.0",
            "BSD 2-Clause License",
            "BSD 3-Clause License",
        ],
    },

    "has_topics": {
        "weight":  0.05,
        "enabled": True,
        "description": (
            "Developer tagged their repo = thought about discoverability. "
            "Binary: tagged = bonus, untagged = neutral. "
            "bradtraversy/mern-auth has NO topics despite 350+ stars — correctly penalised."
        ),
        "bonus_if_present": True,
    },
}


# ---------------------------------------------------------------------------
# RANKING CONFIG — Controls how ranker.py sorts scored repos.
# Primary sort: score. Secondary sort: pushed_at date (recency tiebreaker).
# ---------------------------------------------------------------------------

RANKING_CONFIG = {
    "primary_sort":   "score",
    "secondary_sort": "pushed_at",    # ISO date string — used as tiebreaker
    "score_proximity_threshold": 0.05,  # Repos within this score gap are "tied" → recency decides
}


# ---------------------------------------------------------------------------
# SELECTOR CONFIG
# ---------------------------------------------------------------------------

SELECTOR_CONFIG = {
    "default_top_n": 10,
}
