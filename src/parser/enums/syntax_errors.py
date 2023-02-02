from enum import Enum


class SyntaxErrors(Enum):
    ILLEGAL = "illegal"
    DISCARDED = "discarded"
    MISSING = "missing"
    UNEXPECTED_EOF = "Unexpected EOF"

    def __str__(self) -> str:
        return f"syntax error , {self.value}"
