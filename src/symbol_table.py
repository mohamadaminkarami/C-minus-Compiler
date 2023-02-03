from typing import List, Set
from constants import KEYWORDS


class SymbolTableRow:
    def __init__(self, lexeme: str, address: int) -> None:
        self.lexeme = lexeme
        self.address = address

    def __str__(self) -> str:
        return f"address: {self.address}, lexeme: {self.lexeme}"


class SymbolTable:
    def __init__(self) -> None:
        self._table: List[SymbolTableRow] = [
            SymbolTableRow(lexeme=lexeme, address=-1) for lexeme in KEYWORDS
        ]
        self.current_address = 0

    def does_lexeme_exist(self, lexeme: str):
        for row in self._table:
            if row.lexeme == lexeme:
                return True
        return False

    def add_row(self, lexeme: str):
        row = SymbolTableRow(lexeme=lexeme, address=self.current_address)
        self._table.append(row)
        self.increase_address()

    def get_row(self, lexeme: str) -> SymbolTableRow:
        for row in self._table:
            if row.lexeme == lexeme:
                return row
        raise Exception(f"lexeme {lexeme} does not exist.")

    def find_address(self, lexeme: str):
        return self.get_row(lexeme).address

    def increase_address(self, num=4):
        self.current_address += num

    def __str__(self) -> str:
        s = f"current_address: {self.current_address}\n"
        for row in self._table:
            if row.address != -1:
                s += str(row)
                s += "\n"

        return s


symbol_table = SymbolTable()
