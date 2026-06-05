"""
Educational Value Analysis Module
--------------------------------------------
This Module analyzes the educational value of a repository based on its README content and file structure. 
It extracts learning aspects such as (JWT authentication, database integration, etc.) and verifies if the repository actually content those aspects in the README and file structure. 
The educational value score is calculated based on the presence of these aspects and their representation in the documentation and code organization.

Job: - Extract educational aspects from README and verify using file structure
Input: Repository data including README content and file tree
Output: Educational value score for each repository between 0 and 1, where 1 indicates high educational value
"""

import re
from typing import Dict, List, Optional, Tuple


# ============================================================================
# HELPER FUNCTIONS - FEATURE EXTRACTION
# ============================================================================

def features_extraction(readme_content: Optional[str]) -> Dict[str, bool]:
    """
    Extract educational features from the Features section of README content.
    
    Identifies the Features section in the README and extracts all listed items.
    Supports multiple formats:
    - Markdown bullet points (- feature, * feature)
    - Numbered lists (1. feature, 2. feature)
    
    Args:
        readme_content: The README content (can be HTML or markdown text)
    
    Returns:
        Dictionary with extracted feature names as keys and True as values
    """
    features = {}
    
    if not readme_content:
        return features
    
    # Find the Features section
    # Match headers like "## Features", "# Features", "### Key Features", etc.
    features_section_match = re.search(
        r'#{1,6}\s*(?:key\s+)?features?(?:\s|$|:)',
        readme_content,
        re.IGNORECASE
    )
    
    if not features_section_match:
        return features
    
    # Extract content from Features section to the next main section
    start_pos = features_section_match.end()
    
    # Look for the next section header or horizontal rule
    # This marks the end of Features section
    next_section_match = re.search(
        r'\n(?:#{1,6}\s+|---\s*$)',
        readme_content[start_pos:],
        re.MULTILINE
    )
    
    if next_section_match:
        end_pos = start_pos + next_section_match.start()
    else:
        end_pos = len(readme_content)
    
    features_section = readme_content[start_pos:end_pos]
    
    # Split by lines and process each line
    lines = features_section.split('\n')
    
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue
        
        # Extract bullet points (- or *)
        bullet_match = re.match(r'^\s*[-*]\s+(.+)$', line)
        if bullet_match:
            feature_text = bullet_match.group(1)
        else:
            # Extract numbered lists (1., 2., etc.)
            numbered_match = re.match(r'^\s*\d+\.\s+(.+)$', line)
            if numbered_match:
                feature_text = numbered_match.group(1)
            else:
                # Not a list item, skip
                continue
        
        # Clean up the feature text
        # Remove inline code blocks
        cleaned = re.sub(r'`[^`]+`', '', feature_text)
        # Remove markdown link syntax [text](url) but keep the text
        cleaned = re.sub(r'\[([^\]]+)\]\([^\)]*\)', r'\1', cleaned)
        # Remove markdown bold/italic markers
        cleaned = re.sub(r'\*\*(.+?)\*\*', r'\1', cleaned)
        cleaned = re.sub(r'__(.+?)__', r'\1', cleaned)
        cleaned = re.sub(r'\*(.+?)\*', r'\1', cleaned)
        cleaned = re.sub(r'_(.+?)_', r'\1', cleaned)
        # Remove any remaining special markdown characters
        cleaned = re.sub(r'[`~]', '', cleaned)
        # Trim whitespace
        cleaned = cleaned.strip()
        
        # Only include meaningful features
        if cleaned and len(cleaned) > 2:
            features[cleaned] = True
    
    return features


# ============================================================================
# HELPER FUNCTIONS - FEATURE VERIFICATION
# ============================================================================

def verify_features(features: Dict[str, bool], file_structure: Optional[List[Dict]]) -> Dict[str, bool]:
    """
    Verify extracted features using the file tree structure.
    
    Matches feature names from README against actual files/folders in the repository.
    Uses keyword matching and similarity to find corresponding implementations.
    
    Example: 
    - Feature "JWT Authentication" → looks for auth, jwt, passport, oauth files
    - Feature "MongoDB Integration" → looks for db, mongo, model, schema files
    
    Args:
        features: Dictionary of extracted feature names
        file_structure: List of file/folder dicts with 'path' and 'type' keys
    
    Returns:
        Dictionary with verified features (True if found in file structure)
    """
    verified_features = {key: False for key in features.keys()}
    
    if not file_structure or not features:
        return verified_features
    
    # Create a searchable lowercase paths string
    all_paths = ' '.join([item.get('path', '').lower() for item in file_structure])
    
    # Helper function to extract keywords from feature name
    def extract_keywords(feature_name: str) -> List[str]:
        """Extract important keywords from feature name."""
        # Convert to lowercase and split
        keywords = feature_name.lower().split()
        
        # Filter out common words
        common_words = {'and', 'or', 'the', 'a', 'an', 'with', 'using', 'of', 'in', 'for'}
        keywords = [kw for kw in keywords if kw not in common_words and len(kw) > 2]
        
        return keywords
    
    # Helper function to check if feature exists in file structure
    def feature_exists_in_structure(feature_name: str, all_paths: str) -> bool:
        """Check if a feature likely exists in the file structure."""
        keywords = extract_keywords(feature_name)
        
        if not keywords:
            return False
        
        # Check if at least one keyword matches a path component
        matches = 0
        for keyword in keywords:
            # Search for keyword as a standalone word or part of a path component
            if re.search(rf'\b{re.escape(keyword)}\b', all_paths, re.IGNORECASE) or \
               re.search(rf'{re.escape(keyword)}', all_paths, re.IGNORECASE):
                matches += 1
        
        # Consider verified if at least 50% of keywords are found (or if any keyword matches for short names)
        match_threshold = max(1, len(keywords) // 2)
        return matches >= match_threshold or (len(keywords) == 1 and matches > 0)
    
    # Verify each feature
    for feature in features.keys():
        if features.get(feature, False):  # Only verify if feature was mentioned
            if feature_exists_in_structure(feature, all_paths):
                verified_features[feature] = True
    
    return verified_features


# ============================================================================
# SCORING FUNCTION
# ============================================================================

def calculate_educational_score(features: Dict[str, bool], verified_features: Dict[str, bool]) -> Tuple[float, Dict]:
    """
    Calculate educational value score based on feature presence and verification.
    
    Scoring logic:
    - If feature is mentioned AND verified in file structure: +2 points
    - If feature is mentioned but NOT verified: +0.5 points (incomplete implementation)
    - If feature is not mentioned: 0 points
    
    Args:
        features: Dictionary of extracted features from README
        verified_features: Dictionary of features verified in file structure
    
    Returns:
        Tuple of (score: 0-1, breakdown: dict with feature details)
    """
    breakdown = {}
    total_possible_points = len(features) * 2  # Max 2 points per feature
    earned_points = 0
    
    for feature in features.keys():
        if verified_features.get(feature, False):
            # Feature mentioned and verified: +2 points
            earned_points += 2
            breakdown[feature] = {'mentioned': True, 'verified': True, 'score': 2}
        elif features.get(feature, False):
            # Feature mentioned but not verified: +0.5 points
            earned_points += 0.5
            breakdown[feature] = {'mentioned': True, 'verified': False, 'score': 0.5}
        else:
            # Feature not mentioned: 0 points
            breakdown[feature] = {'mentioned': False, 'verified': False, 'score': 0}
    
    # Normalize score to 0-1 range
    score = earned_points / total_possible_points if total_possible_points > 0 else 0.0
    score = max(0.0, min(1.0, score))
    
    return round(score, 4), breakdown


# ============================================================================
# CENTRAL CALCULATION FUNCTION
# ============================================================================

def calculate_repo_educational_value(repo: Dict) -> Dict:
    """
    Calculate overall educational value score for a single repository.
    
    Process:
    1. Extract features from README content
    2. Verify features exist in file structure
    3. Calculate score based on presence and verification
    
    Args:
        repo: Repository dictionary containing 'readme_content' and 'file_structure'
    
    Returns:
        Dictionary with:
        - 'score': Overall educational value score (0-1)
        - 'breakdown': Detailed breakdown of scoring components
    """
    # Step 1: Extract features from README
    extracted_features = features_extraction(repo.get('readme_content'))
    
    # Step 2: Verify features using file structure
    verified_features = verify_features(extracted_features, repo.get('file_structure'))
    
    # Step 3: Calculate score
    score, score_breakdown = calculate_educational_score(extracted_features, verified_features)
    
    breakdown = {
        'extracted_features': extracted_features,
        'verified_features': verified_features,
        'feature_breakdown': score_breakdown,
        'educational_value_score': score,
    }
    
    return {
        'educational_score': score,
        'breakdown': breakdown,
    }


# ============================================================================
# ORCHESTRATION FUNCTION
# ============================================================================

def analyze_repositories_educational_value(repositories: List[Dict]) -> List[Dict]:
    """
    Orchestration function that processes multiple repositories and adds educational value scores.
    
    Takes a list of repository dictionaries, calculates educational value for each,
    and adds the result in repo['educational_value'].
    
    Args:
        repositories: List of repository dictionaries
    
    Returns:
        List of repositories with 'EDUCATIONAL_VALUE' key added to each
    """
    for repo in repositories:
        # Calculate educational value for this repo
        educational_value_result = calculate_repo_educational_value(repo)
        
        # Add result to repo dict
        repo['educational_value'] = educational_value_result
    
    return repositories

