# Token types
#
# EOF (end-of-file) token is used to indicate that there is no more input left
# Lexical analysis
INTEGER, PLUS, EOF = "INTEGER", "PLUS", "EOF"


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value : [1-9] | + | None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return "Token({type}, {value})".format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # The input program/calculation provided by the user
        self.text = text
        # Index into the program/calculation
        self.pos = 0
        # Current token instance
        self.current_token = None

    def error(self, str):
        raise Exception(str)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer).

        This method is responsible for breaking a sentence apart into tokens.
        One token at a time.
        """
        text = self.text

        # Is `self.pos` index past the end of the `self.text`?
        # If so, then retrun `EOF` token because there is no more calculation/program left.
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]

        # If the current character is digit, return `INTEGER`
        if current_char.isdigit():
            self.pos += 1
            return Token(INTEGER, int(current_char))

        # if the current character is `+`, return `PLUS`
        if current_char == "+":
            self.pos += 1
            return Token(PLUS, current_char)

        self.error(
            "Parsing failed, unknown symbol {symbol}".format(symbol=current_char)
        )

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        left_operand = self.get_next_token()
        if left_operand.type != INTEGER:
            self.error(
                "Sytax Error: expected integer got {symbol}".format(
                    symbol=left_operand.value
                )
            )

        operand = self.get_next_token()
        if operand.type != PLUS:
            self.error(
                "Sytax Error: expected '+' got {symbol}".format(symbol=operand.value)
            )

        right_operand = self.get_next_token()
        if right_operand.type != INTEGER:
            self.error(
                "Sytax Error: expected integer got {symbol}".format(
                    symbol=right_operand.value
                )
            )

        return left_operand.value + right_operand.value


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
