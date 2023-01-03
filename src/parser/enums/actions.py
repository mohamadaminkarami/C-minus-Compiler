from enum import Enum
from typing import Tuple


class Actions(Enum):
    SHIFT = "shift"
    REDUCE = "reduce"
    GOTO = "goto"
    ACCEPT = "accept"

    @staticmethod
    def get_action_and_next_state(action_str: str) -> Tuple["Actions", str]:
        if action_str == Actions.ACCEPT.value:
            return Actions.ACCEPT, ""

        action, next_state = action_str.split("_")

        if action == Actions.SHIFT.value:
            return Actions.SHIFT, next_state
        elif action == Actions.GOTO.value:
            return Actions.GOTO, next_state

        return Actions.REDUCE, next_state
