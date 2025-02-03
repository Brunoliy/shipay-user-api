"""Common algorithms module.
"""
from re import sub


def to_snake_case(expression: str) -> str:
    expression = sub("(.)([A-Z][a-z]+)", r"\1_\2", expression)
    return sub("([a-z0-9])([A-Z])", r"\1_\2", expression).lower()
