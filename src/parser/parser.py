from typing import List
from IO_handler import IO_handler
from scanner.enums.token import TokenType
from error_handler import error_handler
from parser.enums import Actions, SyntaxErrors
from scanner import Scanner
from anytree import Node
from parser.utils import Table, Stack
from code_gen import CodeGenerator
from symbol_table import symbol_table


class Parser:
    INITIAL_STATE = "0"
    FILE_NAME = "16"

    def __init__(self) -> None:
        self.table = Table()
        self.stack = Stack()
        self.stack.push(self.INITIAL_STATE)

        self.tree = Stack()

        self.scanner = Scanner(IO_handler.read_input(self.FILE_NAME))
        self._set_next_token()

        self._last_tree_nodes: List[Node] = []
        self._parent_node = None

        self._code_gen = CodeGenerator()

        self.CODE_GEN_STATES = self._code_gen.get_code_gen_states()

    def _get_line_number(self):
        return self.scanner.line_number

    def _set_next_token(self):
        self.current_token = self.scanner.get_next_token()

    def _get_current_token_str(self):
        if self.current_token.token_type in [TokenType.NUM, TokenType.ID]:
            return str(self.current_token.token_type)

        return self.current_token.lexeme

    def _handle_reduce(self, state: str):
        left_hand_side, right_hand_side = self.table.grammar(state)

        right_hand_side_length = (
            0 if "epsilon" in right_hand_side else len(right_hand_side)
        )

        # tree
        parent = Node(left_hand_side)
        if right_hand_side_length == 0:
            child = Node("epsilon", parent=parent)

        children = self.tree.muliti_pop(right_hand_side_length)

        for child in children:
            child.parent = parent
        self.tree.push(parent)

        # stack
        self.stack.muliti_pop(2 * right_hand_side_length)
        s = self.stack.get()
        self.stack.push(left_hand_side)
        _, next_state = self.table.parse_table(s, left_hand_side)
        self.stack.push(next_state)

    def _handle_code_gen(self, state: str):
        self._code_gen.generate(state, self.current_token.lexeme)

    def _handle_action(self, action: Actions, state: str) -> bool:
        if action == Actions.ACCEPT:
            child = self.tree.pop()
            parent = self.tree.get()
            child.parent = parent

            return True

        elif action == Actions.REDUCE:
            if state in self.CODE_GEN_STATES:
                self._handle_code_gen(state)
                self._code_gen.print_ss()
                self._code_gen.print_pb()
                print("table", symbol_table)
            self._handle_reduce(state)

        elif action == Actions.SHIFT:
            self.tree.push(Node(str(self.current_token)))
            self.stack.push(self.current_token)
            self.stack.push(state)
            self._set_next_token()

        return False

    def _get_panic_non_terminal_and_next_state(self, goto):
        for non_terminal, next_state in goto:
            if self._get_current_token_str() in self.table.follow(non_terminal):
                return non_terminal, next_state

        return None, None

    def _panic(self) -> bool:
        if self.current_token.token_type == TokenType.EOF:
            error_handler.write_syntax_error(
                f"#{self._get_line_number()} : {str(SyntaxErrors.UNEXPECTED_EOF)}"
            )
            self.tree = Stack()
            return True

        error_handler.write_syntax_error(
            f"#{self._get_line_number()} : {str(SyntaxErrors.ILLEGAL)} {self.current_token.lexeme}"
        )
        self._set_next_token()  # skip current token

        # find state with non empty goto
        state = self.stack.get()
        goto = self.table.goto(state)
        while not goto:
            self.tree.pop()
            self.stack.pop()
            error_handler.write_syntax_error(
                f"{str(SyntaxErrors.DISCARDED)} {self.stack.pop()} from stack"
            )
            state = self.stack.get()
            goto = self.table.goto(state)

        # 3
        non_terminal, next_state = self._get_panic_non_terminal_and_next_state(goto)
        while not non_terminal:
            if self.current_token.token_type == TokenType.EOF:
                error_handler.write_syntax_error(
                    f"#{self._get_line_number()} : {str(SyntaxErrors.UNEXPECTED_EOF)}"
                )
                self.tree = Stack()
                return True
            error_handler.write_syntax_error(
                f"#{self._get_line_number()} : {str(SyntaxErrors.DISCARDED)} {self.current_token.lexeme} from input"
            )
            self._set_next_token()
            non_terminal, next_state = self._get_panic_non_terminal_and_next_state(goto)

        self.stack.push(non_terminal)
        self.stack.push(next_state)
        self.tree.push(Node(str(non_terminal)))
        error_handler.write_syntax_error(
            f"#{self._get_line_number()} : {str(SyntaxErrors.MISSING)} {non_terminal}"
        )
        return False

    def parse(self):
        while True:
            state = self.stack.get()
            try:
                action, next_state = self.table.parse_table(
                    state, self._get_current_token_str()
                )
                is_finished = self._handle_action(action, next_state)
                if is_finished:
                    return
            except KeyError as e:
                is_finished = self._panic()

                if is_finished:
                    return

    def get_program_block(self):
        return self._code_gen._pb
