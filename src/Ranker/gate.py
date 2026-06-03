"""
gate.py — Ranker Layer: Gate
-----------------------------
First pass. Drops repos outside bounds defined in weights.GATES.
Only repos passing ALL enabled gates proceed to scorer.py.

Job: filter. Nothing else.
Input:  list of repo dicts from GitHub Layer
Output: (passed_repos, dropped_repos)
"""

from .weights import GATES


def check_single_gate(repo: dict, field: str, config: dict) -> tuple[bool, str]:
    """
    Check a single gate condition for a single repo.

    Returns:
        (passed, reason) — reason is empty string if passed
    """
    value = repo.get(field)

    if value is None:
        return False, f"Missing value for gate field '{field}'"

    gate_min = config.get("gate_min", float("-inf"))
    gate_max = config.get("gate_max", float("inf"))

    if value < gate_min:
        return False, f"Value {value} below gate_min {gate_min}"

    if value > gate_max:
        return False, f"Value {value} above gate_max {gate_max}"

    return True, ""


def apply_gates(repos: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Run all enabled gates against every repo.
    Uses for...else — else block only runs if no break occurred (repo passed all gates).

    Parameters:
        repos: raw list of repo dicts from GitHub Layer

    Returns:
        (passed_repos, dropped_repos)
        dropped_repos entries include title, failed field, and reason
    """
    passed_repos  = []
    dropped_repos = []

    for repo in repos:
        for field, config in GATES.items():
            if not config.get("enabled", True):
                continue

            passed, reason = check_single_gate(repo, field, config)

            if not passed:
                dropped_repos.append({
                    "title":  repo.get("title", "unknown"),
                    "field":  field,
                    "reason": reason,
                })
                break   # Failed a gate — stop checking, don't add to passed
        else:
            passed_repos.append(repo)   # All gates passed

    # Summary
    print(f"\n[gate] {len(repos)} in → {len(passed_repos)} passed, {len(dropped_repos)} dropped")
    for d in dropped_repos:
        print(f"  ✗ '{d['title']}' failed gate '{d['field']}': {d['reason']}")

    return passed_repos, dropped_repos