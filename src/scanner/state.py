from abc import ABC, abstractmethod
from enum import Enum

KEYWORDS = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return', 'endif']
SYMBOLS = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '==', '<']
WHITESPACE = [' ', '\n', '\r', '\t', '\v', '\f']


def is_accepted_character(c):
    return c.isalnum() or c in SYMBOLS or c in WHITESPACE or c == '/'


class LexicalError(Enum):
    INVALID_INPUT = 'Invalid input'
    UNCLOSED_COMMENT = 'Unclosed comment'
    UNMATCHED_COMMENT = 'Unmatched comment'
    INVALID_NUMBER = 'Invalid number'


class State(ABC):
    @abstractmethod
    def get_next_token(self, c):
        pass


class StateInitial(State):
    def get_next_token(self, c):
        if c.isalpha():
            return StateID
        elif c.isdigit():
            return StateNum
        elif c in SYMBOLS:
            return StateSymbol if c == '=' or c == '*' else State.END  # symbols that need lookahead
        elif c == '/':
            return StateUndecided
        else:
            return StateEnd


class StateOneLineComment(State):
    def get_next_token(self, c):
        if c == '\n':
            return StateEnd


class StateMultiLineComment(State):
    def get_next_token(self, c):
        if c == '*':
            return StateMultiLineCommentEnd


class StateMultiLineCommentEnd(State):
    def get_next_token(self, c):
        if c == '/':
            return StateEnd
        elif c != '*':
            return StateMultiLineComment


class StateID(State):
    def get_next_token(self, c):
        if not c.isalnum() and is_accepted_character(c):
            return StateEnd
        elif not is_accepted_character(c):
            return LexicalError.INVALID_INPUT


class StateNum(State):
    def get_next_token(self, c):
        if not c.isdigit():
            if c.isalpha() or not is_accepted_character(c):
                return LexicalError.INVALID_NUMBER
            else:
                return StateEnd


class StateUndecided(State):
    def get_next_token(self, c):
        print("I can roar")


class StateEnd(State):
    def get_next_token(self, c):
        if c == '/':
            return StateOneLineComment
        elif c == '*':
            return StateMultiLineComment
        else:
            return LexicalError.INVALID_NUMBER


class StateSymbol(State):
    def get_next_token(self, c):
        if token.content == '*/' or not is_accepted_character(c):
            return LexicalError.INVALID_NUMBER
        elif not token.content == '==' and is_accepted_character(c):
            return StateEnd
