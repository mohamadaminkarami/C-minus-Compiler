from collections import defaultdict
from typing import Dict, List, Tuple


class ErrorHandler:
    def __init__(self) -> None:
        self._lexical_errors: Dict[int, List[Tuple[str, str]]] = defaultdict(list)
        self._syntax_errors: List[str] = []

    def write_syntax_error(self, error_message: str):
        print(error_message)
        self._syntax_errors.append(error_message)

    def write_lexical_error(self, line_number: int, lexeme: str, error_message: str):
        self._lexical_errors[line_number].append((lexeme, error_message))


error_handler = ErrorHandler()
