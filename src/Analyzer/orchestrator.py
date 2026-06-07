
from .readme_analyzer import analyze_readme
from .tree_analyzer import analyze_tree
from .constant import README_WEIGHTS, TREE_WEIGHTS


def analyze_single_repository(repo: dict) -> dict:
    readme_analysis = analyze_readme(repo.get("readme_content"))
    tree_analysis = analyze_tree(repo.get("file_structure"))

    readme_score = (
        readme_analysis["has_purpose"] * README_WEIGHTS["has_purpose"] +
        readme_analysis["has_installation"] * README_WEIGHTS["has_installation"] +
        readme_analysis["has_features"] * README_WEIGHTS["has_features"] +
        readme_analysis["is_live_deployed"] * README_WEIGHTS["is_live_deployed"]
    )

    tree_score = (
        tree_analysis["has_src"] * TREE_WEIGHTS["has_src"] +
        tree_analysis["has_tests"] * TREE_WEIGHTS["has_tests"] +
        tree_analysis["has_docs"] * TREE_WEIGHTS["has_docs"] +
        tree_analysis["has_config"] * TREE_WEIGHTS["has_config"] +
        tree_analysis["has_ci"] * TREE_WEIGHTS["has_ci"] +
        (tree_analysis["max_depth"] / 10) * TREE_WEIGHTS["depth"]
    )

    content_score = (readme_score + tree_score) / 2
    

    return {
        "content_score": content_score,
        "readme_score": readme_score,
        "tree_score": tree_score,
        "readme_analysis": readme_analysis,
        "tree_analysis": tree_analysis,
    }

def analyze_repository_content(repos: list[dict]) -> list[dict]:
    
    for repo in repos:
        analysis = analyze_single_repository(repo)
        for key, value in analysis.items():
            repo[key] = value

    return repos