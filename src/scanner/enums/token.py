from enum import Enum


class TokenType(Enum):
    NUM = "NUM"
    ID = "ID"
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    EOF = "EOF"

    def __str__(self) -> str:
        return self.value

    def should_be_return(self):
        return self not in [TokenType.COMMENT, TokenType.WHITESPACE]
