from ctypes import sizeof
import json
from typing import Dict, List, Tuple
from IO_handler import IO_handler
from scanner.enums.token import TokenType
from symbol_table import SymbolTableRow, symbol_table
from error_handler import error_handler
from parser.enums import Actions, SyntaxErrors
from scanner import Scanner, Token
from anytree import Node, RenderTree


class Stack:
    def __init__(self) -> None:
        self._stack = []

    def get(self):
        return self._stack[-1] if len(self._stack) else None

    def pop(self):
        return self._stack.pop()

    def muliti_pop(self, num: int):
        if num:
            self._stack = self._stack[:-num]

    def push(self, x):
        self._stack.append(x)

    def __str__(self) -> str:
        return ", ".join(str(a) for a in self._stack)


class Table:
    TABLE_PATH = "src/parser/assets/table.json"

    def __init__(self) -> None:
        self._table = json.load(open(self.TABLE_PATH))

    def first(self, symbol: str) -> List[str]:
        return self._table["first"][symbol]

    def follow(self, symbol: str) -> List[str]:
        return self._table["follow"][symbol]

    def parse_table(self, state: str, token: str):
        return Actions.get_action_and_next_state(
            self._table["parse_table"][state][token]
        )

    def goto(self, state: str) -> List[Tuple[str, str]]:
        return [
            (key, Actions.get_action_and_next_state(value)[1])
            for key, value in filter(
                lambda x: "goto" in x[1],
                sorted(self._table["parse_table"][state].items()),
            )
        ]

    def grammar(self, state: str) -> Tuple[str, List[str]]:
        grammar: List[str] = self._table["grammar"][state]
        return grammar[0], grammar[2:]


class Parser:
    TABLE_PATH = "src/parser/assets/table.json"
    INITIAL_STATE = "0"

    def __init__(self) -> None:
        self.table = Table()
        self.stack = Stack()
        self.stack.push(self.INITIAL_STATE)

        self.scanner = Scanner(IO_handler.read_input("01"))
        self._set_next_token()

        self._last_tree_nodes: List[Node] = []
        self._parent_node = None

    def _get_line_number(self):
        return self.scanner.line_number

    def _set_next_token(self):
        self.current_token = self.scanner.get_next_token()

    def _get_current_token_str(self):
        if self.current_token.token_type in [TokenType.NUM, TokenType.ID]:
            return str(self.current_token.token_type)

        return self.current_token.lexeme

    def _handle_parse_tree(self, right_hand_side_nodes: List[Node]):
        parent = right_hand_side_nodes[-1]
        self._parent_node = parent
        for node in self._last_tree_nodes:
            node.parent = parent

    def _handle_action(self, action: Actions, state: str) -> int:
        if action == Actions.ACCEPT:
            return True

        elif action == Actions.REDUCE:
            left_hand_side, right_hand_side = self.table.grammar(state)
            print(right_hand_side)
            print(self.stack)
            print("------------------------")
            right_hand_side_nodes = [Node(i) for i in right_hand_side]
            self._handle_parse_tree(right_hand_side_nodes)
            self._last_tree_nodes = right_hand_side_nodes

            pop_size = 2 * len(right_hand_side)
            if "epsilon" in right_hand_side:
                pop_size = 0
            self.stack.muliti_pop(pop_size)
            s = self.stack.get()
            self.stack.push(left_hand_side)
            _, next_state = self.table.parse_table(s, left_hand_side)
            self.stack.push(next_state)

        elif action == Actions.SHIFT:
            self.stack.push(self.current_token)
            self.stack.push(state)
            self._set_next_token()

        return False

    def _get_panic_non_terminal_and_next_state(self, goto):
        for non_terminal, next_state in goto:
            if self._get_current_token_str() in self.table.follow(non_terminal):
                return non_terminal, next_state

        return None, None

    def _panic(self) -> int:
        if self.current_token.token_type == TokenType.EOF:
            error_handler.write_syntax_error(
                f"#{self._get_line_number()} : {str(SyntaxErrors.UNXEPECTED_EOF)}"
            )
            return 1
        error_handler.write_syntax_error(
            f"#{self._get_line_number()} : {str(SyntaxErrors.ILLEGAL)} {self.current_token.lexeme}"
        )
        self._set_next_token()  # skip current token

        # find state with non empty goto
        state = self.stack.get()
        goto = self.table.goto(state)
        while not goto:
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
                    f"#{self._get_line_number()} : {str(SyntaxErrors.UNXEPECTED_EOF)}"
                )
                return 1
            error_handler.write_syntax_error(
                f"#{self._get_line_number()} : {str(SyntaxErrors.DISCARDED)} {self.current_token.lexeme} from input"
            )
            self._set_next_token()
            non_terminal, next_state = self._get_panic_non_terminal_and_next_state(goto)

        self.stack.push(non_terminal)
        self.stack.push(next_state)
        error_handler.write_syntax_error(
            f"#{self._get_line_number()} : {str(SyntaxErrors.MISSING)} {non_terminal}"
        )
        return 0

    def parse(self):
        while True:
            state = self.stack.get()

            try:
                action, next_state = self.table.parse_table(
                    state, self._get_current_token_str()
                )
                is_finished = self._handle_action(action, next_state)
                if is_finished:
                    # for pre, fill, node in RenderTree(self._parent_node):
                    #     print("%s%s" % (pre, node.name))
                    return
            except KeyError as e:
                # print(state, self.current_token)
                # return
                is_finished = self._panic()

                if is_finished:
                    # for pre, fill, node in RenderTree(self._parent_node):
                    #     print("%s%s" % (pre, node.name))
                    return
