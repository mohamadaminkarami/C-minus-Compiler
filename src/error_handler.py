from xml.dom.pulldom import ErrorHandler


class _ErrorHandler:
    def __init__(self) -> None:
        self._has_lexical_error = False

        self._lexical_errors_file = open("lexical_errors.txt", "w+")

    def write_lexical_error(self, line_number: int, error_message: str):
        pass

    def close_file(self):
        if not self._has_lexical_error:
            self._lexical_errors_file.write("There is no lexical error.")
        self._lexical_errors_file.close()


error_handler = ErrorHandler()
