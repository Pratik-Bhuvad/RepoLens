from .constants import PROGRAMMING_LANGUAGES, FRAMEWORK_TO_LANGUAGE

def validate_query(query: str) -> tuple[bool, str | None]:
    """
    Validate the search query.
    
    Parameters:
        query (str): The search query string
    
    Returns:
        tuple: (is_valid: bool, error_message: str | None)
    """
    if not query or not query.strip():
        return False, "Query cannot be empty."
    
    if len(query) > 75:
        return False, "Query must not exceed 75 characters."
    
    return True, None


def validate_language(language: str | None) -> tuple[bool, str | None]:
    """
    Validate the programming language.
    
    Parameters:
        language (str | None): The programming language (optional)
    
    Returns:
        tuple: (is_valid: bool, error_message: str | None)
    """
    if language is None or language == "":
        return True, None  # Language is optional
    
    language_lower = language.lower().strip()
    
    if language_lower in PROGRAMMING_LANGUAGES or language_lower in FRAMEWORK_TO_LANGUAGE:
        return True, None
    
    return False, f"Language '{language}' is not a valid programming language or framework."


def validate_stars(min_stars: int | None, max_stars: int | None) -> tuple[bool, str | None]:
    """
    Validate the star range.
    
    Parameters:
        min_stars (int | None): Minimum stars
        max_stars (int | None): Maximum stars
    
    Returns:
        tuple: (is_valid: bool, error_message: str | None)
    """
    # Check if min_stars is valid
    if min_stars is not None:
        if min_stars < 0:
            return False, "Minimum stars cannot be less than 0."
        if min_stars > 1000:
            return False, "Minimum stars cannot be greater than 1000."
    
    # Check if max_stars is valid
    if max_stars is not None:
        if max_stars < 0:
            return False, "Maximum stars cannot be less than 0."
        if max_stars > 1000:
            return False, "Maximum stars cannot be greater than 1000."
    
    # Check if min_stars < max_stars
    if min_stars is not None and max_stars is not None:
        if min_stars > max_stars:
            return False, "Minimum stars cannot be greater than maximum stars."
    
    return True, None


def validate_last_updated(months: int | None) -> tuple[bool, str | None]:
    """
    Validate the last updated input (in months).
    
    Parameters:
        months (int | None): Number of months back from today
    
    Returns:
        tuple: (is_valid: bool, error_message: str | None)
    """
    if months is None:
        return True, None  # last_updated is optional
    
    if not isinstance(months, int):
        return False, "Last updated must be an integer representing number of months."
    
    if months < 0:
        return False, "Last updated cannot be a negative number of months."
    
    return True, None


def validate_all_inputs(query: str, language: str | None, min_stars: int | None, 
                       max_stars: int | None, last_updated_months: int | None) -> tuple[bool, str | None]:
    """
    Validate all inputs together.
    
    Parameters:
        query (str): The search query
        language (str | None): The programming language (optional)
        min_stars (int | None): Minimum stars
        max_stars (int | None): Maximum stars
        last_updated_months (int | None): Last updated in months
    
    Returns:
        tuple: (is_valid: bool, error_message: str | None)
    """
    # Validate query
    is_valid, error = validate_query(query)
    if not is_valid:
        return False, error
    
    # Validate language
    is_valid, error = validate_language(language)
    if not is_valid:
        return False, error
    
    # Validate stars
    is_valid, error = validate_stars(min_stars, max_stars)
    if not is_valid:
        return False, error
    
    # Validate last_updated
    is_valid, error = validate_last_updated(last_updated_months)
    if not is_valid:
        return False, error
    
    return True, None
