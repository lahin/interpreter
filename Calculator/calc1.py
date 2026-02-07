import operator

# Token types
#
# EOF (end-of-file) token is used to indicate that there is no more input left
# Lexical analysis
INTEGER, OPERATOR, EOF = "INTEGER", "OPERATOR", "EOF"


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, OPERATOR, or EOF
        self.type = type
        # token value : [1-9] | + | None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(OPERATOR, '+')
        """
        return "Token({type}, {value})".format(type=self.type, value=repr(self.value))

    __repr__ = __str__


class Interpreter(object):
    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }

    def __init__(self, text):
        # The input program/calculation provided by the user
        self.text = text
        # Index into the program/calculation
        self.pos = 0

    def error(self, err_str):
        raise Exception(err_str)

    def get_integer(self):
        text = self.text
        start = self.pos
        while self.pos < len(text) and text[self.pos].isdigit():
            self.pos += 1
        return int(text[start : self.pos])

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer).

        This method is responsible for breaking a sentence apart into tokens.
        One token at a time.
        """
        text = self.text

        # Skip spaces and tabs
        while self.pos < len(text) and text[self.pos].isspace():
            self.pos += 1

        # Is `self.pos` index past the end of the `self.text`?
        # If so, then retrun `EOF` token because there is no more calculation/program left.
        if self.pos >= len(text):
            return Token(EOF, None)

        current_char = text[self.pos]

        if current_char.isdigit():
            return Token(INTEGER, self.get_integer())

        op = Interpreter.operators.get(current_char)
        if not op is None:
            self.pos += 1
            return Token(OPERATOR, op)

        self.error(f"Parsing failed, unknown symbol {current_char!r}")

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        left_operand = self.get_next_token()
        if left_operand.type != INTEGER:
            self.error(f"Sytax Error: expected integer got {left_operand!r}")

        op = self.get_next_token()
        if op.type != OPERATOR:
            self.error(f"Sytax Error: expected operand got {op!r}")

        right_operand = self.get_next_token()
        if right_operand.type != INTEGER:
            self.error(f"Sytax Error: expected integer got {right_operand!r}")

        return op.value(left_operand.value, right_operand.value)


def main():
    while True:
        try:
            text = input("calc> ")
        except EOFError:
            break

        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()
