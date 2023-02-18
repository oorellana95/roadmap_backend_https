from typing import Optional, List

from project.exceptions.validation_exception import InputValidationException


def query_param_to_list_str(query_param_value: Optional[str]) -> List[str]:
    """Given a query_param as string, return the list of strings of this query_param."""
    return None if query_param_value is None else query_param_value.split(',')


def query_param_to_list_int(query_param_key: str, query_param_value: Optional[str]) -> List[int]:
    """Given a query_param as string, return the list of integers of this query_param as string."""
    try:
        return None if query_param_value is None else list(map(int, query_param_value.split(',')))
    except ValueError:
        raise InputValidationException(f"Missing or incorrect query param {query_param_key}. "
                                       f"All values must be valid numbers")
