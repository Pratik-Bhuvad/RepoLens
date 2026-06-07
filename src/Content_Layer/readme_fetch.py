"""
readme_fetch.py: Module to fetch README files from GitHub repositories.
----------------------------------------------------------------------------------

Job: Fetch readme content for each repository, and attach it to the repo dict for later analysis.
Input: Single repo dict with 'contents_url' field (from GitHub Layer)
Output: Same repo dict with 'readme_content' field added (raw text or None)
"""

import base64
import requests

def clean_content(content: str) -> str:
    """
    Clean README content by removing markdown syntax and normalizing whitespace.
    
    Parameters:
        content (str): The raw README content as a string.
        
    Returns:
        str: The cleaned README content.
    """
    # For simplicity, this function just normalizes whitespace.
    # More complex cleaning (e.g. removing markdown) can be added later.
    content = content.replace('\r\n', '')  # Normalize newlines
    return ' '.join(content.split())

def decode_readme_content(encoded_content: str) -> str:
    """
    Decode base64-encoded README content from GitHub API.
    
    Parameters:
        encoded_content (str): The base64-encoded content string from GitHub API.
        
    Returns:
        str: The decoded README content as a UTF-8 string, or None if decoding fails.
    """
    try:
        decoded_bytes = base64.b64decode(encoded_content)
        return decoded_bytes.decode('utf-8', errors='replace')
    except (base64.binascii.Error, UnicodeDecodeError):
        return None
    
def fetch_readme_content(repo: dict, headers: dict) -> dict:
    """
    Fetch the README content for a given repository using its contents_url.
    Parameters:
        repo (dict): A repository dictionary containing at least the 'contents_url' field.
        headers (dict): Headers to include in the API request (e.g. for authentication).
        
    Returns:
        dict : The updated repository dictionary with 'readme_content' field added, or None if fetching fails.
    """
    owner = repo.get('owner', {})
    title = repo.get('title', 'unknown')
    
    readme_url = f"https://api.github.com/repos/{owner}/{title}/readme"
    
    try:
        response = requests.get(readme_url, headers=headers, timeout=10)
            
        response.raise_for_status()
        data = response.json()
        
        if 'content' in data and data.get('encoding') == 'base64':
            
            decoded_content = decode_readme_content(data['content'])

            text = clean_content(decoded_content) if decoded_content else None

            return {'text': text}
        else:
            return {'text': None}
            
    except (requests.RequestException, ValueError) as e:
        return {'text': None}