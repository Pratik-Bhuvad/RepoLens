"""
gate.py — Ranker Layer: Gate
-----------------------------
First pass. Drops repos that fall outside the bounds defined in score_weights.GATES.
Only repos that pass ALL enabled gates proceed to scorer.py.
 
Job: filter. Nothing else.
Input:  list of repo dicts (from GitHub Layer)
Output: list of repo dicts that passed all gates
"""
 
from .weights import GATES

def check_single_gate(repo: dict, field: str, config: dict) -> tuple[bool, str]:
    """
    Check if a single gate condition is satisfied for a repo.
    
    Parameters:
        - repo: dict containing repo data
        - field: the gate field to check (e.g. "stars")
        - config: dict with gate configuration (enabled, gate_min, gate_max)
        
    Returns:
        - True if the repo passes the gate, False otherwise
        - Reason string if the gate is failed, empty string if passed
    """
    value = repo.get(field)
    
    if value is None:
        return False, f"Missing value for gate field '{field}'"
    
    if value < config.get("gate_min", float("-inf")):
        return False, f"Value {value} below gate_min {config['gate_min']}"
    
    if value > config.get("gate_max", float("inf")):
        return False, f"Value {value} above gate_max {config['gate_max']}"
    
    return True, ""

def apply_gates(repos: list[dict]) -> list[dict]:
    """
    Run all enabled gates against every repo.
    Repos that fail any gate are dropped.
 
    Parameters:
        repos: raw list of repo dicts from GitHub Layer
 
    Returns:
        filtered list of repo dicts
    """
    passed_repos = []
    dropped_repos = []
    
    for repo in repos['repositories']:
        for field, config in GATES.items():
            if config.get("enabled", True):
                passed, reason = check_single_gate(repo, field, config)
                print(f"Checking repo '{repo['title']}' for gate '{field}': value={repo.get(field)}, passed={passed}, reason='{reason}'")
                if not passed:
                    dropped_repos.append((repo["title"], field, reason))
                    break  # Stop checking other gates for this repo
        else:
            passed_repos.append(repo)
    return passed_repos, dropped_repos
                   