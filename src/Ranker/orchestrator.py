from .gate import apply_gates

"""
ORCHESTRATOR — Main entry point for the ranking process.
Job: orchestrate the entire ranking pipeline: apply gates, then score.
Input: list of repo dicts (from GitHub Layer)
Output: list of scored repo dicts, sorted by final score
"""

def orchestrate_ranking_pipeline(repos: list[dict]) -> list[dict]:
    # Step 1: Apply gates to filter out repos that don't meet criteria
    passed_repos, dropped_repos = apply_gates(repos)
    
    print(f"Passed {len(passed_repos)} repos, dropped {len(dropped_repos)} repos based on gates.")
        
    return passed_repos