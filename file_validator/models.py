from typing import TypedDict

class ValidationIssue(TypedDict):
    row: int
    field: str
    code: str
    message: str