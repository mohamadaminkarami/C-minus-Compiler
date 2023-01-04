import json
from typing import List, Tuple
from parser.enums import Actions


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
