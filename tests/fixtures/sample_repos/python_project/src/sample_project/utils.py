"""Utility functions."""

import re
from typing import Any


def validate_email(email: str) -> bool:
    """Validate email format.

    Args:
        email: Email address to validate

    Returns:
        True if valid email format
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def sanitize_input(value: str) -> str:
    """Sanitize user input.

    Args:
        value: Input string to sanitize

    Returns:
        Sanitized string
    """
    # Remove leading/trailing whitespace
    value = value.strip()
    # Remove potential SQL injection characters
    value = re.sub(r"[;'\"]", "", value)
    return value


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Deep merge two dictionaries.

    Args:
        base: Base dictionary
        override: Dictionary to merge on top

    Returns:
        Merged dictionary
    """
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result
