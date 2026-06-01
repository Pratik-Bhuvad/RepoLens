from .weights import SCORE_WEIGHTS

# ---------------------------------------------------------------------------
# WEIGHT VALIDATION — Sanity check that scored weights sum to 1.0.
# Run this when modifying weights.
# ---------------------------------------------------------------------------
 
def validate_weights() -> bool:
    total = sum(
        v["weight"]
        for v in SCORE_WEIGHTS.values()
        if v.get("enabled", True)
    )
    is_valid = abs(total - 1.0) < 1e-9
    if not is_valid:
        print(f"[score_weights] WARNING: Enabled weights sum to {total:.4f}, expected 1.0")
    return is_valid

validate_weights()