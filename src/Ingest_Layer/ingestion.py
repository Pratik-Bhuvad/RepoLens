from ..config import parser_config
from .validator import validate_all_inputs
from .converters import map_framework_to_language, months_to_date


def ingest_data() -> dict | None:
    """
        Ingest data from the terminal and validate all inputs.
        
        Parameters:
            None
        
        Returns:
            dict | None: A dictionary containing the ingested and validated data, or None if invalid
    """
    args = parser_config().parse_args()
    
    # Validate all inputs
    is_valid, error_message = validate_all_inputs(
        query=args.query,
        language=args.language,
        min_stars=args.min_stars,
        max_stars=args.max_stars,
        last_updated_months=args.last_updated_months,
    )
    
    if not is_valid:
        print(f"Error: {error_message}")
        return None
    
    # Map framework to language if provided
    language = args.language
    if language:
        mapped_language = map_framework_to_language(language)
        if mapped_language:
            language = mapped_language
    
    # Convert months to date if provided
    last_updated = None
    if args.last_updated_months is not None:
        last_updated = months_to_date(args.last_updated_months)
    
    # Prepare the data dictionary
    data = {
        "query": args.query.strip(),
        "language": language,
        "min_stars": args.min_stars,
        "max_stars": args.max_stars,
        "last_updated": last_updated,
    }
    
    return data