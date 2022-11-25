from scanner.enums import TokenType
from scanner.symbol_table import SymbolTable


class Scanner:
    def __init__(self) -> None:
        self.line_number = 0
        self._current_state = 0
        self._symbol_table = SymbolTable()

        self._start_cursor = 0
        self._end_cursor = 0

    def _get_next_state():
        return NotImplemented

    def get_next_token() -> TokenType:
        return NotImplemented
