"""
score_weights.py — Ranker Layer Configuration
----------------------------------------------
This file defines HOW repos are scored, not the scoring logic itself.
The actual computation lives in ranker.py.
 
Each weight entry defines:
    - weight      : relative importance in the final score (all weights sum to 1.0)
    - enabled     : toggle a signal on/off without deleting config
    - description : why this signal matters
    - invert      : True if a LOWER raw value = better score (e.g. fork_star_ratio)
    - gate        : if True, this field filters repos BEFORE scoring (not a scored field)
    - gate_min    : minimum allowed value (gate fields only)
    - gate_max    : maximum allowed value (gate fields only)
"""
 
# ---------------------------------------------------------------------------
# GATES — Applied before scoring. Repos outside these bounds are dropped.
# These fields do NOT contribute to the score.
# ---------------------------------------------------------------------------
 
GATES = {
    "stars": {
        "enabled": True,
        "gate_min": 10,
        "gate_max": 500,
        "description": (
            "Minimum proves the repo isn't invisible. "
            "Maximum avoids famous/over-known repos. "
            "Stars are NOT scored — only used as a gate. "
            "Scoring stars rewards tutorial creators with large audiences."
        ),
    },
    "size_kb": {
        "enabled": True,
        "gate_min": 50,       # Below this = likely a small demo or skeleton
        "gate_max": 50_000,    # Above this = too large to read and learn from
        "description": (
            "Filters out repos that are either too minimal to learn from "
            "or too large to navigate as a beginner."
        ),
    },
}
 
 
# ---------------------------------------------------------------------------
# SCORED FIELDS — These contribute to the final rank score.
# All weights must sum to 1.0.
# ---------------------------------------------------------------------------
 
SCORE_WEIGHTS = {
 
    "fork_star_ratio": {
        "weight": 0.35,
        "enabled": True,
        "invert": True,
        "description": (
            "Core tutorial detector. Tutorial repos get forked heavily by students "
            "following along — real projects get starred more than forked. "
            "A LOW ratio means more stars per fork = real project signal. "
            "Invert=True because lower ratio → higher score. "
            "Minimum of 10 stars required before this ratio is meaningful."
        ),
        "minimum_stars_to_apply": 10,
    },
 
    "open_issues": {
        "weight": 0.30,
        "enabled": True,
        "invert": False,
        "description": (
            "Best underrated signal. Real projects have issues filed because "
            "real people used them and hit real problems. "
            "Tutorials rarely have issues — students rewatch the video, not file bugs. "
            "Sweet spot: 1–20 issues. Cap scoring at 20 to avoid rewarding broken repos."
        ),
        "score_cap": 20,       # Issues beyond this don't add more score
        "zero_penalty": False, # 0 issues = neutral (not penalised) — small repos can be clean
    },
 
    "forks": {
        "weight": 0.15,
        "enabled": True,
        "invert": False,
        "description": (
            "Raw fork count as a secondary engagement signal. "
            "Used alongside fork_star_ratio, not instead of it. "
            "Diminishing returns applied — a repo with 200 forks shouldn't "
            "dominate one with 40 forks. Score is log-scaled in ranker.py."
        ),
        "scale": "log",        # Hint to ranker.py to apply log scaling
    },
 
    "license": {
        "weight": 0.10,
        "enabled": True,
        "invert": False,
        "description": (
            "A developer who added a license was thinking about others using their code. "
            "Builder mindset indicator. Absence is neutral — many real beginner "
            "projects skip licensing. Presence is a small positive signal only."
        ),
        "bonus_if_present": True,   # Binary: present = bonus, absent = 0 (not penalised)
        "preferred_licenses": [     # These score higher than generic/no license
            "MIT License",
            "Apache License 2.0",
            "GNU General Public License v3.0",
        ],
    },
 
    "has_topics": {
        "weight": 0.05,
        "enabled": True,
        "invert": False,
        "description": (
            "A developer who tagged their repo thought about discoverability. "
            "Binary signal — tagged repos get a small bonus. "
            "Notable: bradtraversy/mern-auth has NO topics despite 350+ stars, "
            "which correctly reduces its score here."
        ),
        "bonus_if_present": True,
    },
 
    "owner_type": {
        "weight": 0.05,
        "enabled": True,
        "invert": False,
        "description": (
            "Organization repos are almost never tutorials. "
            "A company or open source org maintaining a project is a strong "
            "real-project signal. Binary: Organization = bonus, User = neutral."
        ),
        "bonus_value": "Organization",  # Ranker checks repo['owner_type'] == this
    },
}
 