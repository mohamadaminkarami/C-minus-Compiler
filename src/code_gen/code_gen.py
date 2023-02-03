from symbol_table import symbol_table, SymbolTableRow


class Actions:
    ADD = "ADD"
    MULT = "MULT"
    DIV = "DIV"
    SUB = "SUB"
    EQ = "EQ"
    LT = "LT"
    ASSIGN = "ASSIGN"
    JPF = "JPF"
    JP = "JP"
    PRINT = "PRINT"

    @classmethod
    def get_action_from_operand(cls, operand):
        if operand == "<":
            return cls.LT
        elif operand == "==":
            return cls.EQ
        elif operand == "+":
            return cls.ADD
        elif operand == "-":
            return cls.SUB
        elif operand == "*":
            return cls.MULT
        elif operand == "/":
            return cls.DIV

        raise Exception("invalid operand")


class AddressCode:
    def __init__(self, action, k1, k2=None, k3=None) -> None:
        self.action = action
        self.k1 = k1
        self.k2 = k2 if k2 != None else " "
        self.k3 = k3 if k3 != None else " "

    def __str__(self) -> str:
        return f"({self.action}, {self.k1}, {self.k2}, {self.k3} )"


class CodeGenerator:
    def __init__(self) -> None:
        self.mapping = {
            "28": self._pop,
            "31": self._jpf,
            "32": self._jp,
            "33": self._while,
            "42": self._assign,
            "45": self._arr_element,
            "46": self._op,
            "50": self._op,
            "54": self._op,
            "62": self._print,
            "67": self._pid,
            "68": self._size_array,
            "69": self._push,
            "70": self._save,
            "71": self._jpf_save,
            "72": self._switch,
            "73": self._case,
            "74": self._default,
            "75": self._label,
        }
        self._symbol_table_next_addr = 0
        self._temp_addr = 500

        self._ss = []

        self._pb = []

        self._is_first_case = True

    @property
    def top(self):
        return len(self._ss) - 1

    @property
    def i(self):
        return len(self._pb)

    def generate(self, state: str, input: str):
        print(self.mapping[state].__name__, input)
        self.mapping[state](input)

    def get_code_gen_states(self):
        return self.mapping.keys()

    def _pid(self, lexeme):
        if not symbol_table.does_lexeme_exist(lexeme):
            symbol_table.add_row(lexeme=lexeme)

        self._ss.append(symbol_table.find_address(lexeme=lexeme))

    def _size_array(self, length_str):
        array_length = int(length_str)
        symbol_table.increase_address(4 * (array_length - 1))

    def _assign(self, _):
        top = self.top
        self._pb.append(AddressCode(Actions.ASSIGN, self._ss[top], self._ss[top - 1]))
        rhs = self._ss[top]
        self._ss.pop()
        self._ss.pop()
        self._ss.append(rhs)

    def _push(self, lexeme: str):
        if lexeme.isnumeric():
            lexeme = f"#{lexeme}"
        self._ss.append(lexeme)

    def _get_temp(self):
        temp = self._temp_addr
        self._temp_addr += 4
        return temp

    def _save(self, _):
        self._ss.append(self.i)
        self._pb.append(None)

    def _jpf_save(self, _):
        top = self.top

        self._pb[self._ss[top]] = AddressCode(
            Actions.JPF,
            self._ss[top - 1],
            self.i + 1,
        )
        self._ss.pop()
        self._ss.pop()
        self._ss.append(self.i)
        self._pb.append(None)

    def _jpf(self, _):
        top = self.top
        self._pb[self._ss[top]] = AddressCode(Actions.JPF, self._ss[top - 1], self.i)
        self._ss.pop()
        self._ss.pop()

    def _jp(self, _):
        top = self.top
        self._pb[self._ss[top]] = AddressCode(
            Actions.JP,
            self.i,
        )
        self._ss.pop()

    def _op(self, _):
        top = self.top
        action = Actions.get_action_from_operand(self._ss[top - 1])
        temp = self._get_temp()
        self._pb.append(AddressCode(action, self._ss[top - 2], self._ss[top], temp))
        self._ss.pop()
        self._ss.pop()
        self._ss.pop()
        self._ss.append(temp)

    def _print(self, _):
        self._pb.append(AddressCode(Actions.PRINT, self._ss[self.top]))
        self._ss.pop()
        # self._ss.pop()

    def _switch(self, _):
        self._is_first_case = True

    def _case(self, num_str: str):
        num = f"#{num_str}"
        if not self._is_first_case:
            self._default(num_str)

        top = self.top
        temp = self._get_temp()
        self._pb.append(AddressCode(Actions.EQ, self._ss[top], num, temp))
        self._ss.append(temp)
        self._ss.append(self.i)
        self._pb.append(None)
        self._is_first_case = False

    def _arr_element(self, _):
        top = self.top
        temp1 = self._get_temp()
        self._pb.append(AddressCode(Actions.MULT, self._ss[top], "#4", temp1))
        temp2 = self._get_temp()
        self._pb.append(AddressCode(Actions.ADD, f"#{self._ss[top - 1]}", temp1, temp2))
        self._ss.pop()
        self._ss.pop()
        self._ss.append(f"@{temp2}")

    def _default(self, _):
        top = self.top
        self._pb[self._ss[top]] = AddressCode(
            Actions.JPF,
            self._ss[top - 1],
            self.i,
        )
        self._ss.pop()
        self._ss.pop()

    def _while(self, _):
        top = self.top
        self._pb[self._ss[top]] = AddressCode(
            Actions.JPF,
            self._ss[top - 1],
            self.i + 1,
        )
        self._pb.append(AddressCode(Actions.JP, self._ss[top - 2]))
        self._ss.pop()
        self._ss.pop()
        self._ss.pop()

    def _pop(self, _):
        self._ss.pop()

    def _label(self, _):
        self._ss.append(self.i)

    def print_ss(self):

        print("ss: ", self._ss)

    def print_pb(self):

        for index, block in enumerate(self._pb):
            print(f"{index}\t {str(block)}")
