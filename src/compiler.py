from scanner.enums.token import TokenType
from scanner.scanner import Scanner
from IO_handler import IO_handler
from symbol_table import SymbolTableRow, symbol_table
from error_handler import error_handler


if __name__ == "__main__":
    scanner = Scanner(IO_handler.read_input("15"))

    while not scanner.is_eof():
        token_type, lexeme = scanner.get_next_token()
        if token_type == TokenType.ID:
            if not symbol_table.is_lexeme_exist(lexeme):
                symbol_table.add_row(SymbolTableRow(lexeme))

    IO_handler.write_tokens(scanner.tokens)
    IO_handler.write_symbol_tables(list(symbol_table._table))
    IO_handler.write_lexical_errors(error_handler._lexical_errors)
