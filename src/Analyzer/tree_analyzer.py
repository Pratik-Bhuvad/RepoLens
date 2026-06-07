"""
content/analyzers/tree_analyzer.py
"""


def analyze_tree(file_structure: list[dict] | None) -> dict:

    breakdown = {
        "max_depth": 0,
        "breadth": 0,

        "has_src": False,
        "has_tests": False,
        "has_docs": False,
        "has_config": False,
        "has_ci": False,

        "file_count": 0,
        "folder_count": 0,
    }

    if not file_structure:
        return breakdown

    paths = []

    for item in file_structure:

        path = item.get("path", "").lower()

        paths.append(path)

        if item.get("type") == "blob":
            breakdown["file_count"] += 1

        elif item.get("type") == "tree":
            breakdown["folder_count"] += 1

    # depth

    if paths:
        breakdown["max_depth"] = max(
            p.count("/")
            for p in paths
        )

    # breadth

    top_level = set()

    for path in paths:

        parts = path.split("/")

        if len(parts) > 1:
            top_level.add(parts[0])

    breakdown["breadth"] = len(top_level)

    # signals

    breakdown["has_src"] = any(
        p.startswith(("src/", "lib/"))
        for p in paths
    )

    breakdown["has_tests"] = any(
        k in p
        for p in paths
        for k in (
            "test",
            "tests",
            "__tests__",
            "spec",
        )
    )

    breakdown["has_docs"] = any(
        k in p
        for p in paths
        for k in (
            "docs",
            "documentation",
        )
    )

    breakdown["has_config"] = any(
        k in p
        for p in paths
        for k in (
            "config",
            ".env",
            "settings",
        )
    )

    breakdown["has_ci"] = any(
        ".github/workflows"
        in p
        for p in paths
    )

    return breakdown