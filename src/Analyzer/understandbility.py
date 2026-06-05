"""
Understandability Analyzer
--------------------------------------
This module calculates the understandability of the codebase using readme content and file tree

Job: Analyze the understandability of each repository based on its readme and file structure
Input: Repository data including readme content and file tree
Output: Understandability score for each repository between 0 and 1, where 1 indicates high understandability
"""

import re
from typing import Dict, List, Optional, Tuple


# ============================================================================
# HELPER FUNCTIONS - README ANALYSIS
# ============================================================================

def _calculate_readme_score(readme_content: Optional[str]) -> Tuple[float, Dict[str, bool]]:
    """
    Calculate README understandability score based on presence of key sections.
    
    Looks for key sections in README:
    - Installation
    - Usage
    - Features
    - Architecture
    - Screenshots
    
    Args:
        readme_content: The README content (can be HTML or markdown text)
    
    Returns:
        Tuple of (score: 0-1, breakdown: dict with section presence)
    """
    breakdown = {
        'has_installation': False,
        'has_usage': False,
        'has_features': False,
        'has_architecture': False,
        'has_screenshots': False,
    }
    
    if not readme_content:
        return 0.0, breakdown
    
    # Convert to lowercase for case-insensitive matching
    content_lower = readme_content.lower()
    
    # Check for Installation section (including quick start variations)
    if re.search(r'(^|\n|>)\s*#{1,3}\s*installation|install\s*guide|getting\s*started|quick\s*start', content_lower):
        breakdown['has_installation'] = True
    
    # Check for Usage section
    if re.search(r'(^|\n|>)\s*#{1,3}\s*usage|how\s*to\s*use|quick\s*start', content_lower):
        breakdown['has_usage'] = True
    
    # Check for Features section (headers, key features, or tabular/list format)
    features_header = re.search(r'(^|\n|>)\s*#{1,3}\s*features?|key\s*features', content_lower)
    features_table = re.search(r'\|\s*feature|<table>|<ul>|\n\s*[-*]\s+\w+\s*:', content_lower)
    if features_header or features_table:
        breakdown['has_features'] = True
    
    # Check for Architecture section
    if re.search(r'(^|\n|>)\s*#{1,3}\s*architecture|system\s*design|project\s*structure', content_lower):
        breakdown['has_architecture'] = True
    
    # Check for Screenshots section
    if re.search(r'(^|\n|>)\s*#{1,3}\s*screenshots?|demo|video', content_lower) or \
       'img src=' in content_lower or '<img' in content_lower:
        breakdown['has_screenshots'] = True
    
    # Calculate score: 1 point per section found (max 5)
    sections_found = sum(breakdown.values())
    score = sections_found / 5.0  # Normalize to 0-1
    
    return score, breakdown


# ============================================================================
# HELPER FUNCTIONS - FILE STRUCTURE ANALYSIS
# ============================================================================

def _calculate_tree_score(file_structure: Optional[List[Dict]]) -> Tuple[float, Dict]:
    """
    Calculate file structure understandability score based on depth and breadth.
    
    Evaluates:
    - Tree depth (how organized the structure is)
    - Tree breadth (distribution of files)
    - Presence of key organizational patterns
    
    Args:
        file_structure: List of file/folder dicts with 'path' and 'type' keys
    
    Returns:
        Tuple of (score: 0-1, breakdown: dict with metrics)
    """
    breakdown = {
        'depth': 0,
        'breadth': 0,
        'has_organized_structure': False,
        'has_src_or_lib': False,
        'has_config': False,
        'has_docs': False,
        'has_tests': False,
        'file_count': 0,
        'folder_count': 0,
    }
    
    if not file_structure:
        return 0.0, breakdown
    
    # Count files and folders, track paths
    paths = []
    for item in file_structure:
        path = item.get('path', '')
        item_type = item.get('type', '')
        
        if item_type == 'tree':
            breakdown['folder_count'] += 1
        elif item_type == 'blob':
            breakdown['file_count'] += 1
        
        paths.append(path.lower())
    
    # Calculate depth: count directory levels (/)
    max_depth = 0
    if paths:
        max_depth = max(path.count('/') for path in paths)
    breakdown['depth'] = max_depth
    
    # Calculate breadth: average files per depth level
    if paths:
        breakdown['breadth'] = len([p for p in paths if p.count('/') <= 2])
    
    # Check for organized structure patterns
    organized_keywords = ['src', 'lib', 'source', 'app', 'modules', 'components']
    if any(keyword in ' '.join(paths) for keyword in organized_keywords):
        breakdown['has_organized_structure'] = True
    
    # Check for src/lib
    if any(p.startswith(('src/', 'lib/')) for p in paths):
        breakdown['has_src_or_lib'] = True
    
    # Check for config files/folders
    config_keywords = ['config', 'env', 'settings', '.env']
    if any(keyword in ' '.join(paths) for keyword in config_keywords):
        breakdown['has_config'] = True
    
    # Check for docs
    doc_keywords = ['docs', 'documentation', 'readme', '.md']
    if any(keyword in ' '.join(paths) for keyword in doc_keywords):
        breakdown['has_docs'] = True
    
    # Check for tests
    test_keywords = ['test', 'spec', '__tests__', 'tests']
    if any(keyword in ' '.join(paths) for keyword in test_keywords):
        breakdown['has_tests'] = True
    
    # Calculate composite score
    score_components = [
        min(max_depth / 5.0, 1.0),  # Depth score (normalized to max 5 levels)
        min(breakdown['breadth'] / 20.0, 1.0),  # Breadth score (normalized to 20 files)
        float(breakdown['has_organized_structure']),
        float(breakdown['has_src_or_lib']) * 0.3,
        float(breakdown['has_config']) * 0.2,
        float(breakdown['has_docs']) * 0.3,
        float(breakdown['has_tests']) * 0.3,
    ]
    
    score = sum(score_components) / len(score_components)
    score = min(score, 1.0)  # Cap at 1.0
    
    return score, breakdown


# ============================================================================
# CENTRAL CALCULATION FUNCTION
# ============================================================================

def calculate_repo_understandability(repo: Dict) -> Dict:
    """
    Calculate overall understandability score for a single repository.
    
    Combines:
    - README documentation score (40% weight)
    - File structure organization score (60% weight)
    
    Args:
        repo: Repository dictionary containing 'readme_content' and 'file_structure'
    
    Returns:
        Dictionary with:
        - 'score': Overall understandability score (0-1)
        - 'breakdown': Detailed breakdown of scoring components
    """
    readme_score, readme_breakdown = _calculate_readme_score(
        repo.get('readme_content')
    )
    
    tree_score, tree_breakdown = _calculate_tree_score(
        repo.get('file_structure')
    )
    
    # Weighted combination: README 40%, Tree 60%
    overall_score = (readme_score * 0.4) + (tree_score * 0.6)
    
    # Ensure score is between 0 and 1
    overall_score = max(0.0, min(1.0, overall_score))
    
    breakdown = {
        'readme_score': round(readme_score, 4),
        'readme_breakdown': readme_breakdown,
        'tree_score': round(tree_score, 4),
        'tree_breakdown': tree_breakdown,
        'understandability_score': round(overall_score, 4),
    }
    
    return {
        'score': round(overall_score, 4),
        'breakdown': breakdown,
    }


# ============================================================================
# ORCHESTRATION FUNCTION
# ============================================================================

def analyze_repositories_understandability(repositories: List[Dict]) -> List[Dict]:
    """
    Orchestration function that processes multiple repositories and adds understandability scores.
    
    Takes a list of repository dictionaries, calculates understandability for each,
    and adds the result in repo['UNDERSTANDABILITY'].
    
    Args:
        repositories: List of repository dictionaries
    
    Returns:
        List of repositories with 'UNDERSTANDABILITY' key added to each
    """
    for repo in repositories:
        # Calculate understandability for this repo
        understandability_result = calculate_repo_understandability(repo)
        
        # Add result to repo dict
        repo['understand'] = understandability_result
    
    return repositories

