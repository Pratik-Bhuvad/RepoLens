from .config import parser_config
from datetime import datetime

def validate_data(data):
    """
        Validate the ingested data
        
        Parameters:
            data (dict): A dictionary containing the ingested data
        
        Returns:
            bool: True if the data is valid, False otherwise
    """
    if data["min_stars"] and data["max_stars"] and data["min_stars"] > data["max_stars"]:
        return False, "Minimum stars cannot be greater than maximum stars."
    if data["last_updated"]:
        try:
            datetime.strptime(data["last_updated"], "%Y-%m-%d")
        except ValueError:
            return False, "Last updated date must be in YYYY-MM-DD format."
    return True, None

def ingest_data():
    """
        Ingest data from the terminal 
        
        Parameters:
            None
        
        Returns:
            dict: A dictionary containing the ingested data
    """
    args = parser_config().parse_args()
    data = {
        "query": args.query,
        "language": args.language,
        "min_stars": args.min_stars,
        "max_stars": args.max_stars,
        "last_updated": args.last_updated,
    }
    is_valid, error_message = validate_data(data)
    if not is_valid:
        print(f"Error: {error_message}")
        return None
    
    return data