class Stack:
    def __init__(self) -> None:
        self._stack = []

    def get(self):
        return self._stack[-1] if len(self._stack) else None

    def pop(self):
        return self._stack.pop()

    def muliti_pop(self, num: int):
        poped = []
        if num:
            poped = self._stack[-num:]
            self._stack = self._stack[:-num]
        return poped

    def push(self, x):
        self._stack.append(x)

    def __str__(self) -> str:
        return ", ".join(str(a) for a in self._stack)
