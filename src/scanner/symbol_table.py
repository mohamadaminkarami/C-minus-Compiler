from typing import List
from scanner.constants import KEYWORDS


class SymbolTableRow:
    def __init__(self, lexeme: str) -> None:
        self.lexeme = lexeme

    def __str__(self) -> str:
        return f"{self.lexeme}"


class SymbolTable:
    def __init__(self) -> None:
        self._table: List[SymbolTableRow] = [
            SymbolTableRow(lexeme) for lexeme in KEYWORDS
        ]

    def add_row(self, symbol_table_row: SymbolTableRow):
        self._table.append(symbol_table_row)
