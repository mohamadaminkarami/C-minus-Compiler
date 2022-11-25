from constants import KEYWORDS


def is_keyword(lexeme: str):
    print(lexeme, lexeme in KEYWORDS, len(lexeme))
    return lexeme in KEYWORDS
