"""
readme_reader.py — Analyzer Layer
-----------------------------------
Fetches the README for a repo and extracts structured signal from it.

Job: read README, return structured data. Nothing else.
Input:  single repo dict (must have contents_url)
Output: readme_data dict or None if README unavailable

"""

import base64
import requests

def _decode_readme(response_json: dict) -> str | None:
    """Decode base64 README content from GitHub API response."""
    try:
        content = response_json.get("content", "")
        # GitHub returns content with newlines inside the base64 string
        cleaned = content.replace("\n", "")
        return base64.b64decode(cleaned).decode("utf-8", errors="replace")
    except Exception:
        return None

def read_readme(repo:dict, headers: dict) -> dict:
    """
    Fetch and decode the README for a repo.

    Parameters:
        repo:    dict containing at least 'contents_url' key
        headers: GitHub API auth headers
        
    Returns:
        dict with 'text' key containing README content, or None if not found
    """
    
    contents_url = repo.get("contents_url", "")
    if not contents_url:
        return {"text": None}

    try:
        # GitHub API: GET /repos/{owner}/{repo}/contents/{path}
        readme_url = contents_url.replace("{+path}", "README.md")
        response = requests.get(readme_url, headers=headers)

        if response.status_code == 404:
            # Try lowercase fallback
            readme_url_lower = contents_url.replace("{+path}", "readme.md")
            response = requests.get(readme_url_lower, headers=headers, timeout=10)
 
        if response.status_code != 200:
            print(f"  [readme_reader] No README found for '{repo.get('title')}'")
            return {"text": None}
        
        text = _decode_readme(response.json())
        if not text:
            print(f"  [readme_reader] README found but failed to decode for '{repo.get('title')}'")
            return {"text": None}
        
        return {"text": text}
        
    except Exception as e:
        print(f"  [readme_reader] Error fetching README for '{repo.get('title')}': {e}")
        return {"text": None}