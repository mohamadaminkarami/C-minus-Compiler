from typing import Dict, List, Tuple
from scanner.enums.token import TokenType

from symbol_table import SymbolTableRow


class IOHandler:
    def read_input(self):
        file = open("input.txt", "r")
        return file.read()

    def _list_to_str(self, l: List[Tuple[str, str]]) -> str:
        s = ""
        for i, v in l:
            s += f"({i}, {v})"

        return s

    def write_lexical_errors(self, lexical_errors: Dict[int, List[Tuple[str, str]]]):
        file = open("lexical_errors.txt", "w+")
        if len(lexical_errors.keys()) == 0:
            file.write("There is no lexical error.")
        else:
            for line_number, lexical_error_list in lexical_errors.items():
                file.write(f"{line_number}.\t{self._list_to_str(lexical_error_list)}\n")

        file.close()

    def write_tokens(self, tokens: Dict[int, List[Tuple[TokenType, str]]]):
        file = open("tokens.txt", "w+")

        for line_number, token_list in tokens.items():
            file.write(f"{line_number}.\t{self._list_to_str(token_list)}\n")

        file.close()

    def write_symbol_tables(self, symbols: List[SymbolTableRow]):
        file = open("symbol_table.txt", "w+")

        for index, symbol_table_row in enumerate(symbols):
            file.write(f"{index + 1}.\t{symbol_table_row}\n")
        file.close()


IO_handler = IOHandler()
