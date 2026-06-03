def build_github_query(data: dict) -> str:
    """
        Build an optimized GitHub query based on the ingested data.
        Input data is a dictionary with language being the primary available filter.
        Uses default values for stars and last_updated if not provided.
        
        Parameters:
            data (dict): A dictionary containing search parameters (language is available)
                        Uses DEFAULT_MIN_STARS, DEFAULT_MAX_STARS, DEFAULT_LAST_UPDATED_MONTHS if not provided
            
        Returns:
            str: An optimized GitHub query string for the Search API
    """
    
    github_query = f"{data.get('query', '')}"
    
    # Add language filter if available
    if 'language' in data and data['language']:
        github_query += f" language:{data['language']}"
        
    if 'min_stars' in data and 'max_stars' in data and data['min_stars'] is not None and data['max_stars'] is not None:
        # Add stars filter
        github_query += f" stars:{data.get('min_stars')}..{data.get('max_stars')}"
    
    # Add last updated filter if available
    github_query += f" pushed:>{data.get('last_updated')}"
    
    github_query += f" fork:false"
    
    
    return github_query.strip()