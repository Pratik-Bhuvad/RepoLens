"""
validate_weights.py — Ranker Layer: Weight Validator
------------------------------------------------------
Run this file directly whenever you modify weights.py.
Catches configuration errors before they silently corrupt scores.

Usage:
    python validate_weights.py
"""

from .weights import SCORE_WEIGHTS, GATES, RANKING_CONFIG, SELECTOR_CONFIG


def validate_score_weights() -> list[str]:
    """Check that enabled weights sum to exactly 1.0."""
    errors = []

    enabled_weights = {
        field: config["weight"]
        for field, config in SCORE_WEIGHTS.items()
        if config.get("enabled", True)
    }

    total = sum(enabled_weights.values())

    if abs(total - 1.0) > 1e-9:
        errors.append(
            f"SCORE_WEIGHTS sum to {total:.6f}, expected 1.0. "
            f"Difference: {total - 1.0:+.6f}\n"
            f"  Enabled fields: { {k: v for k, v in enabled_weights.items()} }"
        )

    return errors


def validate_gates() -> list[str]:
    """Check gate min/max values are logically consistent."""
    errors = []

    for field, config in GATES.items():
        gate_min = config.get("gate_min")
        gate_max = config.get("gate_max")

        if gate_min is not None and gate_max is not None:
            if gate_min >= gate_max:
                errors.append(
                    f"GATES['{field}']: gate_min={gate_min} >= gate_max={gate_max}. "
                    f"No repo can pass this gate."
                )

    return errors


def validate_thresholds() -> list[str]:
    """Check field-level thresholds are sensible."""
    errors = []

    fsr = SCORE_WEIGHTS.get("fork_star_ratio", {})
    min_stars = fsr.get("min_stars_threshold", 0)
    min_forks = fsr.get("min_forks_threshold", 0)

    star_gate_min = GATES.get("stars", {}).get("gate_min", 0)

    if min_stars < star_gate_min:
        errors.append(
            f"fork_star_ratio.min_stars_threshold={min_stars} is below "
            f"GATES['stars'].gate_min={star_gate_min}. "
            f"The ratio threshold will never trigger — all repos already have >= {star_gate_min} stars."
        )

    issues_config = SCORE_WEIGHTS.get("open_issues", {})
    score_cap = issues_config.get("score_cap", 0)
    if score_cap <= 0:
        errors.append(f"open_issues.score_cap={score_cap} must be > 0.")

    forks_config = SCORE_WEIGHTS.get("forks", {})
    log_ceiling = forks_config.get("log_ceiling", 0)
    if log_ceiling <= 0:
        errors.append(f"forks.log_ceiling={log_ceiling} must be > 0.")

    return errors


def validate_ranking_config() -> list[str]:
    """Check ranking config references valid fields."""
    errors = []

    primary = RANKING_CONFIG.get("primary_sort")
    if primary != "score":
        errors.append(
            f"RANKING_CONFIG.primary_sort='{primary}'. "
            f"Expected 'score' — scorer.py always attaches this field."
        )

    threshold = RANKING_CONFIG.get("score_proximity_threshold", 0)
    if not (0.0 < threshold < 1.0):
        errors.append(
            f"RANKING_CONFIG.score_proximity_threshold={threshold} "
            f"must be between 0.0 and 1.0."
        )

    return errors


def validate_selector_config() -> list[str]:
    """Check selector config is sensible."""
    errors = []

    n = SELECTOR_CONFIG.get("default_top_n", 0)
    if n <= 0:
        errors.append(f"SELECTOR_CONFIG.default_top_n={n} must be > 0.")

    return errors


# ---------------------------------------------------------------------------
# Run all validations
# ---------------------------------------------------------------------------

def run_all() -> bool:
    """
    Run every validation check.
    Prints results and returns True if all pass, False if any fail.
    """
    all_errors = []

    checks = [
        ("Score weights sum",     validate_score_weights),
        ("Gate bounds",           validate_gates),
        ("Field thresholds",      validate_thresholds),
        ("Ranking config",        validate_ranking_config),
        ("Selector config",       validate_selector_config),
    ]

    print("\n── Weight Validation ──────────────────────────────")
    for check_name, check_fn in checks:
        errors = check_fn()
        if errors:
            print(f"  ✗ {check_name}")
            for e in errors:
                print(f"      {e}")
            all_errors.extend(errors)
        else:
            print(f"  ✓ {check_name}")

    print("───────────────────────────────────────────────────")
    if all_errors:
        print(f"  {len(all_errors)} error(s) found. Fix weights.py before running.\n")
        return False
    else:
        print("  All checks passed.\n")
        return True


if __name__ == "__main__":
    import sys
    passed = run_all()
    sys.exit(0 if passed else 1)