import argparse
from dotenv import load_dotenv
import os

load_dotenv()

# Default values from environment variables or hardcoded defaults
DEFAULT_MIN_STARS = int(os.getenv("DEFAULT_MIN_STARS"))
DEFAULT_MAX_STARS = int(os.getenv("DEFAULT_MAX_STARS"))
DEFAULT_LAST_UPDATED_MONTHS = os.getenv("DEFAULT_LAST_UPDATED_MONTHS")
GITHUB_URL = os.getenv("Github_url", "https://api.github.com/search/repositories")
GITHUB_HEADER = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f"Bearer {os.getenv('Github_token', '')}"
}
GITHUB_TREE_URL_TEMPLATE = f"https://api.github.com/repos/{{owner}}/{{repo}}/git/trees/{{sha}}?recursive=1"

class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"Error: {message}")
        self.print_help()
        exit(2)


def parser_config():
    """
    Configure and return the argument parser for RepoLens.
    
    Args:
        query (str): Required. The search query for repositories (max 75 chars).
        language (str): Optional. Filter by programming language or framework.
        -ms/--min-stars (int): Minimum number of stars (0-1000). Default: 0.
        -mx/--max-stars (int): Maximum number of stars (0-1000). Default: 100.
        -u/--last-updated (int): Number of months back to filter repositories.
    """
    parser = CustomParser(
        description="RepoLens: A tool for analyzing and visualizing software repositories.",
        epilog="Examples:\n"
               "  python main.py 'machine learning' python -ms 50 -mx 500\n"
               "  python main.py 'web framework' javascript -u 6"
    )
    
    # Required arguments
    parser.add_argument(
        "query",
        type=str,
        help="The search query for repositories (required, max 75 characters)."
    )
    
    # Optional arguments
    parser.add_argument(
        "language",
        type=str,
        nargs='?',
        default=None,
        help="Filter repositories by programming language or framework (optional)."
    )
    
    parser.add_argument(
        "-ms", "--min-stars",
        type=int,
        dest="min_stars",
        help="Filter repositories by minimum number of stars (0-1000, default: 0)."
    )
    
    parser.add_argument(
        "-mx", "--max-stars",
        type=int,
        dest="max_stars",
        help="Filter repositories by maximum number of stars (0-1000, default: 100)."
    )
    
    parser.add_argument(
        "-u", "--last-updated",
        default=DEFAULT_LAST_UPDATED_MONTHS,
        type=int,
        dest="last_updated_months",
        help="Filter repositories updated within the last N months."
    )
    
    return parser