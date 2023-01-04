from typing import IO
from parser.parser import Parser
from scanner.enums.token import TokenType
from scanner.scanner import Scanner
from IO_handler import IO_handler
from symbol_table import SymbolTableRow, symbol_table
from error_handler import error_handler


class Compiler:
    def __init__(self) -> None:
        self.parser = Parser()

    def compile(self):
        self.parser.parse()
        IO_handler.write_syntax_errors(error_handler._syntax_errors)
        IO_handler.write_parse_tree(self.parser.tree.get())


if __name__ == "__main__":
    compiler = Compiler()
    compiler.compile()
