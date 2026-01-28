"""
Input validation and sanitization functions.
Prevents XSS attacks, CSV injection, and invalid data.
"""

import re
from typing import Dict, List, Optional, Tuple
from config import VALIDATION, FUNDING_STAGES, INDUSTRIES


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_required_fields(data: Dict) -> None:
    """
    Validate that required fields are present and non-empty.

    Args:
        data: Dictionary containing company data

    Raises:
        ValidationError: If required fields are missing or empty
    """
    required = ['Company Name', 'Description']
    missing = []

    for field in required:
        value = data.get(field, '').strip()
        if not value:
            missing.append(field)

    if missing:
        raise ValidationError(f"Required fields missing: {', '.join(missing)}")


def validate_string_length(value: str, field_name: str, max_length: int) -> None:
    """
    Validate string field length.

    Args:
        value: String to validate
        field_name: Name of field for error messages
        max_length: Maximum allowed length

    Raises:
        ValidationError: If string exceeds max length
    """
    if len(value) > max_length:
        raise ValidationError(
            f"{field_name} exceeds maximum length of {max_length} characters "
            f"(current: {len(value)})"
        )


def validate_url(url: str, field_name: str) -> None:
    """
    Validate URL format (if provided).

    Args:
        url: URL string to validate
        field_name: Name of field for error messages

    Raises:
        ValidationError: If URL format is invalid
    """
    if not url or not url.strip():
        return  # Empty URLs are allowed (optional field)

    # Basic URL validation - must start with http:// or https://
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )

    if not url_pattern.match(url.strip()):
        raise ValidationError(f"{field_name} must be a valid URL starting with http:// or https://")


def validate_numeric(value: str, field_name: str, min_val: float, max_val: float) -> Optional[float]:
    """
    Validate numeric field.

    Args:
        value: String representation of number
        field_name: Name of field for error messages
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        Parsed float value or None if empty

    Raises:
        ValidationError: If value is not a valid number or out of range
    """
    if not value or not value.strip():
        return None  # Empty numeric fields are allowed

    try:
        num = float(value.strip())
    except ValueError:
        raise ValidationError(f"{field_name} must be a valid number")

    if num < min_val or num > max_val:
        raise ValidationError(
            f"{field_name} must be between {min_val} and {max_val} "
            f"(current: {num})"
        )

    return num


def validate_year(value: str, field_name: str) -> Optional[int]:
    """
    Validate year field.

    Args:
        value: String representation of year
        field_name: Name of field for error messages

    Returns:
        Parsed integer year or None if empty

    Raises:
        ValidationError: If year is invalid
    """
    if not value or not value.strip():
        return None  # Empty year is allowed

    try:
        year = int(value.strip())
    except ValueError:
        raise ValidationError(f"{field_name} must be a valid 4-digit year")

    min_year = VALIDATION['min_founded_year']
    max_year = VALIDATION['max_founded_year']

    if year < min_year or year > max_year:
        raise ValidationError(
            f"{field_name} must be between {min_year} and {max_year} "
            f"(current: {year})"
        )

    return year


def validate_dropdown(value: str, field_name: str, allowed_values: List[str]) -> str:
    """
    Validate dropdown selection.

    Args:
        value: Selected value
        field_name: Name of field for error messages
        allowed_values: List of allowed values

    Returns:
        Validated value (empty string if not provided)

    Raises:
        ValidationError: If value not in allowed list
    """
    if not value or not value.strip():
        return ''  # Empty selection is allowed

    value = value.strip()

    if value not in allowed_values:
        raise ValidationError(
            f"{field_name} must be one of: {', '.join(allowed_values)}"
        )

    return value


def sanitize_html(text: str) -> str:
    """
    Remove HTML tags and script elements to prevent XSS attacks.

    Args:
        text: Input text that may contain HTML

    Returns:
        Sanitized text with HTML removed
    """
    if not text:
        return ''

    # Remove <script> tags and their contents
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Remove all HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Decode common HTML entities
    html_entities = {
        '&lt;': '<',
        '&gt;': '>',
        '&amp;': '&',
        '&quot;': '"',
        '&#39;': "'",
    }

    for entity, char in html_entities.items():
        text = text.replace(entity, char)

    return text.strip()


def prevent_csv_injection(text: str) -> str:
    """
    Prevent CSV injection attacks by prefixing formula characters with single quote.

    Excel and Google Sheets treat cells starting with =, +, -, @ as formulas.
    This can lead to code execution when CSV is opened in spreadsheet software.

    Args:
        text: Input text

    Returns:
        Text with formula characters escaped
    """
    if not text:
        return ''

    text = str(text).strip()

    # Check if text starts with formula characters
    if text and text[0] in ('=', '+', '-', '@'):
        # Prefix with single quote to neutralize formula
        return "'" + text

    return text


def validate_company_data(data: Dict) -> Dict:
    """
    Validate and sanitize all company data fields.

    Args:
        data: Raw company data dictionary

    Returns:
        Validated and sanitized data dictionary

    Raises:
        ValidationError: If validation fails
    """
    # Check required fields first
    validate_required_fields(data)

    # Sanitize and validate each field
    validated = {}

    # Company Name (required)
    company_name = sanitize_html(data.get('Company Name', '').strip())
    validate_string_length(
        company_name,
        'Company Name',
        VALIDATION['company_name_max_length']
    )
    validated['Company Name'] = prevent_csv_injection(company_name)

    # Company LinkedIn (optional URL)
    linkedin_url = data.get('Company LinkedIn', '').strip()
    validate_url(linkedin_url, 'Company LinkedIn')
    validated['Company LinkedIn'] = linkedin_url

    # Founders (optional text)
    founders = sanitize_html(data.get('Founders', '').strip())
    validate_string_length(
        founders,
        'Founders',
        VALIDATION['founders_max_length']
    )
    validated['Founders'] = prevent_csv_injection(founders)

    # China Background (optional text)
    china_bg = sanitize_html(data.get('China Background', '').strip())
    validate_string_length(
        china_bg,
        'China Background',
        VALIDATION['china_background_max_length']
    )
    validated['China Background'] = prevent_csv_injection(china_bg)

    # Total Funding (optional numeric)
    funding = validate_numeric(
        data.get('Total Funding (USD M)', ''),
        'Total Funding (USD M)',
        VALIDATION['min_funding'],
        VALIDATION['max_funding']
    )
    validated['Total Funding (USD M)'] = str(funding) if funding is not None else ''

    # Funding Stage (optional dropdown)
    stage = validate_dropdown(
        data.get('Funding Stage', ''),
        'Funding Stage',
        FUNDING_STAGES
    )
    validated['Funding Stage'] = stage

    # Founded Year (optional year)
    year = validate_year(
        data.get('Founded Year', ''),
        'Founded Year'
    )
    validated['Founded Year'] = str(year) if year is not None else ''

    # Industry (optional dropdown)
    industry = validate_dropdown(
        data.get('Industry', ''),
        'Industry',
        INDUSTRIES
    )
    validated['Industry'] = industry

    # Current Achievements (optional text)
    achievements = sanitize_html(data.get('Current Achievements', '').strip())
    validate_string_length(
        achievements,
        'Current Achievements',
        VALIDATION['achievements_max_length']
    )
    validated['Current Achievements'] = prevent_csv_injection(achievements)

    # Investors (optional text)
    investors = sanitize_html(data.get('Investors', '').strip())
    validate_string_length(
        investors,
        'Investors',
        VALIDATION['investors_max_length']
    )
    validated['Investors'] = prevent_csv_injection(investors)

    # Description (required text)
    description = sanitize_html(data.get('Description', '').strip())
    validate_string_length(
        description,
        'Description',
        VALIDATION['description_max_length']
    )
    validated['Description'] = prevent_csv_injection(description)

    return validated
