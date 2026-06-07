"""
content/analyzers/readme_analyzer.py
"""

from .constant import (
    PURPOSE_PATTERNS,
    INSTALLATION_PATTERNS,
    FEATURE_PATTERNS,
    LIVE_PATTERNS,
    DEPLOYED_DOMAINS,
)


def analyze_readme(readme_content: str | None) -> dict:

    breakdown = {
        "has_purpose": False,
        "has_installation": False,
        "has_features": False,
        "is_live_deployed": False,
    }

    if not readme_content:
        return breakdown

    text = readme_content.lower()

    breakdown["has_purpose"] = any(
        p in text
        for p in PURPOSE_PATTERNS
    )

    breakdown["has_installation"] = any(
        p in text
        for p in INSTALLATION_PATTERNS
    )

    breakdown["has_features"] = any(
        p in text
        for p in FEATURE_PATTERNS
    )

    breakdown["is_live_deployed"] = (
        any(p in text for p in LIVE_PATTERNS)
        or
        any(d in text for d in DEPLOYED_DOMAINS)
    )

    return breakdown
