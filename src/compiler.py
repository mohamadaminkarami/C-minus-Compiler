from scanner.scanner import Scanner
from IO_handler import IO_handler
from symbol_table import symbol_table
from error_handler import error_handler

if __name__ == "__main__":
    input = IO_handler.read_input()

    scanner = Scanner(IO_handler.read_input())

    while not scanner.is_eof():
        scanner.get_next_token()

    IO_handler.write_tokens(scanner.tokens)
    IO_handler.write_symbol_tables(symbol_table._table)
    IO_handler.write_lexical_errors(error_handler._lexical_errors)
