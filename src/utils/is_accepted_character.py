from constants import ALL_SYMBOLS, WHITESPACES


def is_accepted_character(char: str):
    return char.isalnum() or char in ALL_SYMBOLS or char in WHITESPACES
