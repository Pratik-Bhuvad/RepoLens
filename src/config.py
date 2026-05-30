import argparse

def parser_config():
    parser = argparse.ArgumentParser(description="RepoLens: A tool for analyzing and visualizing software repositories.")
    parser.add_argument("query", type=str, help="The search query for repositories.")
    parser.add_argument("language", type=str, help="Filter repositories by programming language.")
    parser.add_argument("stars", type=int, help="Filter repositories by minimum number of stars.")
    parser.add_argument("last_updated", type=str, help="Filter repositories by last updated date (YYYY-MM-DD).")
    
    return parser