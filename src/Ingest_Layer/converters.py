from datetime import datetime
from dateutil.relativedelta import relativedelta
from .constants import FRAMEWORK_TO_LANGUAGE, PROGRAMMING_LANGUAGES


def map_framework_to_language(framework: str) -> str | None:
    """
    Map a framework name to its primary programming language.
    
    Parameters:
        framework (str): The framework name
    
    Returns:
        str | None: The mapped language or None if not found
    """
    if framework is None:
        return None
    
    framework_lower = framework.lower().strip()
    
    if framework_lower in FRAMEWORK_TO_LANGUAGE:
        return FRAMEWORK_TO_LANGUAGE[framework_lower]
    
    if framework_lower in PROGRAMMING_LANGUAGES:
        return framework.capitalize()
    
    return None


def months_to_date(months: int) -> str:
    """
    Convert number of months back to a date string.
    Considers 31/30 days of respective months.
    
    Parameters:
        months (int): Number of months back from today
    
    Returns:
        str: Date string in YYYY-MM-DD format
    """
    if months == 0:
        return datetime.today().strftime("%Y-%m-%d")
    
    # Calculate the date by subtracting months
    target_date = datetime.today() - relativedelta(months=months)
    return target_date.strftime("%Y-%m-%d")
