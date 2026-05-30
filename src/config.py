import argparse
from dotenv import load_dotenv
import os

load_dotenv()
min_stars = int(os.getenv("min-stars"))
max_stars = int(os.getenv("max-stars"))
last_updated = os.getenv("last_updated")

class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"Error: {message}")
        self.print_help()
        exit(2)

def parser_config():
    parser = CustomParser(description="RepoLens: A tool for analyzing and visualizing software repositories.")
    parser.add_argument("query", type=str, help="The search query for repositories.")
    parser.add_argument("language", type=str, nargs='?', help="Filter repositories by programming language.")
    parser.add_argument("-ms","--min-stars", default=min_stars, type=int, help="Filter repositories by minimum number of stars.")
    parser.add_argument("-mx","--max-stars", default=max_stars, type=int, help="Filter repositories by maximum number of stars.")
    parser.add_argument("-u","--last_updated", default=last_updated, type=str, help="Filter repositories by last updated date (YYYY-MM-DD).")
    
    return parser