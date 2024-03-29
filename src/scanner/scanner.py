from collections import defaultdict
from typing import Dict, List, Tuple
from scanner.enums import TokenType
from error_handler import error_handler
from constants import SINGLE_SYMBOLES, WHITESPACES
from scanner.enums.lexical_error import LexicalError
from symbol_table import SymbolTableRow, symbol_table
from dataclasses import dataclass
from utils import is_keyword, is_accepted_character


@dataclass(frozen=True)
class Token:
    lexeme: str
    token_type: TokenType

    def __str__(self) -> str:
        return (
            self.lexeme
            if self.token_type == TokenType.EOF
            else f"({self.token_type.value}, {self.lexeme})"
        )


class Scanner:
    def __init__(self, input: str) -> None:
        self.line_number = 1
        self._current_state = 0
        self._open_comment_line = 1

        self._input = input

        self._start_cursor = 0
        self._end_cursor = 0

        self.tokens: Dict[int, List[Token]] = defaultdict(list)

    def _get_next_state(self, char: str):
        # initial State
        if self._current_state not in [11, 12, 13, 14, 15]:
            if not is_accepted_character(char):
                raise Exception(LexicalError.INVALID_INPUT)

        if self._current_state == 0:
            if char.isdigit():
                return 1  # NUM State
            if char.isalpha():
                return 3  # ID/KEYWORD State
            if char in WHITESPACES:
                return 5
            if char in SINGLE_SYMBOLES:
                return 6
            if char == "=":
                return 7
            if char == "/":
                return 10
            if char == "*":
                return 17

        # NUM State
        if self._current_state == 1:
            if char.isdigit():
                return 1
            if not char.isalnum():
                return 2
            else:
                raise Exception(LexicalError.INVALID_NUMBER)

        # ID/KEYWORD State
        if self._current_state == 3:
            if char.isalnum():
                return 3
            return 4

        if self._current_state == 7:
            if char == "=":
                return 8
            return 9

        if self._current_state == 10:
            self._open_comment_line = self.line_number
            if char == "*":
                return 11
            if char == "/":
                return 14
            return 16

        if self._current_state == 11:
            if char == "*":
                return 12
            return 11

        if self._current_state == 12:
            if char == "*":
                return 12
            if char == "/":
                return 13
            return 11

        if self._current_state == 14:
            if char == "\n" or self.is_eof():
                return 15
            return 14

        if self._current_state == 17:
            if char == "/":
                raise Exception(LexicalError.UNMATCHED_COMMENT)
            return 18

    def _is_final_state(self) -> bool:
        return self._current_state in [2, 4, 5, 6, 8, 9, 13, 15, 16, 18]

    def _handle_extra_char_read(self):
        if self._current_state in [2, 4, 9, 16, 18]:
            self._end_cursor -= 1

    def _get_token_type(self) -> TokenType:
        if self._current_state == 2:
            return TokenType.NUM
        if self._current_state == 4:
            return TokenType.KEYWORD if is_keyword(self._get_lexeme()) else TokenType.ID
        if self._current_state == 5:
            return TokenType.WHITESPACE
        if self._current_state in [6, 8, 9, 16, 18]:
            return TokenType.SYMBOL
        if self._current_state in [13, 15]:
            return TokenType.COMMENT

        raise Exception("_get_token_type should call after _is_final_state")

    def _get_lexeme(self) -> str:
        return self._input[self._start_cursor : self._end_cursor]

    def is_eof(self):
        return len(self._input) == self._end_cursor

    def get_next_token(self) -> Token:
        while not self.is_eof():
            char = self._input[self._end_cursor]
            self._end_cursor += 1
            try:
                self._current_state = self._get_next_state(char)
            except Exception as lexical_error:
                error_handler.write_lexical_error(
                    self.line_number, self._get_lexeme(), str(lexical_error)
                )
                self._start_cursor = self._end_cursor
                self._current_state = 0

            if self._is_final_state():
                self._handle_extra_char_read()
                token_type = self._get_token_type()
                lexeme = self._get_lexeme()
                if token_type == TokenType.ID:
                    if not symbol_table.does_lexeme_exist(lexeme):
                        symbol_table.add_row(lexeme=lexeme)

                self._start_cursor = self._end_cursor
                self._current_state = 0

                if token_type.should_be_return():
                    self.tokens[self.line_number].append(
                        Token(token_type=token_type, lexeme=lexeme)
                    )
                    return Token(lexeme=lexeme, token_type=token_type)
            if char == "\n":
                self.line_number += 1

        if self._current_state in [11, 12]:
            error_handler.write_lexical_error(
                self._open_comment_line,
                f"{self._get_lexeme()[:7]}...",
                str(LexicalError.UNCLOSED_COMMENT),
            )

        return Token(token_type=TokenType.EOF, lexeme="$")
