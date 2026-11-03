import re
from file_validator.models import ValidationIssue

def validate_required_fields(
    rows: list[dict[str, str | None]], 
    required_fields: list[str]
) -> list[ValidationIssue]:
    """
    Validate that the required fields are present in the data.

    Args:
        rows (list of dict): The data to validate.
        required_fields (list of str): The list of required field names.

    Returns:
        list of dict: The validation issues.
    """
    issues = []
    for i, record in enumerate(rows, start=2):
        missing_fields = [
            field 
            for field in required_fields 
            if not (record.get(field) or "").strip()
        ]

        if missing_fields:
            for missing_field in missing_fields:
                issues.append({
                    'row': i,
                    'field': missing_field,
                    'code': 'required_field',
                    'message': f"Required field '{missing_field}' is missing."
                })
    return issues

def validate_unique_fields(
    rows: list[dict[str, str | None]], 
    unique_fields: list[str]
) -> list[ValidationIssue]:
    """
    Validate that the specified fields are unique across the data.

    Args:
        rows (list of dict): The data to validate.
        unique_fields (list of str): The list of field names that should be unique.

    Returns:
        list of dict: The validation issues.
    """
    issues = []
    seen_values = {field: {} for field in unique_fields}

    for i, record in enumerate(rows, start=2):
        for field in unique_fields:
            if not (record.get(field) or "").strip():
                continue  # Skip empty values for uniqueness check

            value = (record.get(field) or "").strip()

            if value in seen_values[field]:
                issues.append({
                    'row': i,
                    'field': field,
                    'code': 'duplicate_value',
                    'message': (
                        f"Duplicate value '{value}' in field '{field}' "
                        f"(first seen at row {seen_values[field][value]})."
                    )
                })
            else:
                seen_values[field][value] = i  # Store value with row number for better error reporting

    return issues

def validate_email_fields(
    rows: list[dict[str, str | None]], 
    email_fields: list[str]
) -> list[ValidationIssue]:
    """
    Validate that the specified fields contain valid email addresses.

    Args:
        rows (list of dict): The data to validate.
        email_fields (list of str): The list of field names that should contain valid email addresses.

    Returns:
        list of dict: The validation issues.
    """
    issues = []
    email_pattern = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")

    for i, record in enumerate(rows, start=2):
        for field in email_fields:
            value = (record.get(field) or "").strip()
            if value and not email_pattern.fullmatch(value):
                issues.append({
                    'row': i,
                    'field': field,
                    'code': 'invalid_email',
                    'message': f"Invalid email format in field '{field}': '{value}'"
                })

    return issues