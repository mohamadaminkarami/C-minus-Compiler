from anytree import Node, RenderTree
from typing import Dict, List, Tuple
from scanner.enums.token import TokenType
from code_gen import Actions
from symbol_table import SymbolTableRow


class IOHandler:
    def read_input(self, num):
        self.num = num

        # file = open(f"../p3_tests/T{num}/input.txt", "r")  # for testing
        file = open(f"input.txt", "r")  # for quera judge

        return file.read()

    def _list_to_str(self, l: List[Tuple[str, str]]) -> str:
        s = ""
        for i, v in l:
            s += f"({i}, {v}) "

        return s

    def write_lexical_errors(self, lexical_errors: Dict[int, List[Tuple[str, str]]]):
        file = open(f"../p3_res/T{self.num}/lexical_errors.txt", "w+")  # for testing
        # file = open(f"lexical_errors.txt", "w+")  # for quera judge

        if len(lexical_errors.keys()) == 0:
            file.write("There is no lexical error.")
        else:
            for line_number, lexical_error_list in lexical_errors.items():
                file.write(f"{line_number}.\t{self._list_to_str(lexical_error_list)}\n")

        file.close()

    def write_tokens(self, tokens: Dict[int, List[Tuple[TokenType, str]]]):
        file = open(f"../p3_res/T{self.num}/tokens.txt", "w+")  # for testing
        # file = open(f"tokens.txt", "w+")  # for quera judge

        for line_number, token_list in tokens.items():
            file.write(f"{line_number}.\t{self._list_to_str(token_list)}\n")

        file.close()

    def write_symbol_tables(self, symbols: List[SymbolTableRow]):
        file = open(f"../p3_res/T{self.num}/symbol_table.txt", "w+")  # for testing
        # file = open(f"symbol_table.txt", "w+")  # for quera judge

        for index, symbol_table_row in enumerate(symbols):
            file.write(f"{index + 1}.\t{symbol_table_row}\n")
        file.close()

    def write_parse_tree(self, parent: Node):
        tree_str = ""
        if parent:
            for pre, fill, node in RenderTree(parent):
                tree_str += "%s%s" % (pre, node.name) + "\n"
        file = open(f"../p3_res/T{self.num}/parse_tree.txt", "w")  # for testing
        # file = open(f"parse_tree.txt", "w+")  # for quera judge
        file.write(tree_str.strip())
        file.close()

    def write_syntax_errors(self, syntax_errors: List[str]):
        file = open(f"../p3_res/T{self.num}/syntax_errors.txt", "w+")  # for testing
        # file = open(f"syntax_errors.txt", "w+")  # for quera judge

        if syntax_errors:
            for message in syntax_errors:
                file.write(f"{message}\n")
        else:
            file.write("There is no syntax error.")
        file.close()

    def write_program_block(self, program_block: List[Actions]):
        # file = open(f"../p3_res/T{self.num}/output.txt", "w+")  # for testing
        # file = open(f"../interpreter/output.txt", "w+")  # for testing
        file = open(f"output.txt", "w+")  # for quera judge
        for index, block in enumerate(program_block):
            file.write(f"{index}.\t{str(block)}\n")

        file.close()

    def write_semantic_errors(self):
        file = open(f"semantic_errors.txt", "w+")  # for quera judge
        file.write("The input program is semantically correct.")
        file.close()


IO_handler = IOHandler()
