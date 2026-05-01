# intermediate_code.py

# -----------------------------------------
# Intermediate Code Generator (TAC)
# -----------------------------------------

class TACGenerator:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.temp_count = 0
        self.code = []

    # -----------------------------------------
    # Helpers
    # -----------------------------------------
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        self.pos += 1

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    # -----------------------------------------
    # Main generation function
    # -----------------------------------------
    def generate(self):
        while self.current_token() is not None:
            token = self.current_token()

            if token.type == "KEYWORD" and token.value == "INT":
                self.handle_declaration()

            elif token.type == "KEYWORD" and token.value == "PRINT":
                self.handle_print()

            else:
                self.advance()

        return self.code

    # -----------------------------------------
    # Handle: INT a = expr
    # -----------------------------------------
    def handle_declaration(self):
        self.advance()  # skip INT

        var_name = self.current_token().value
        self.advance()  # skip identifier

        self.advance()  # skip '='

        result = self.parse_expression()

        # assign result to variable
        self.code.append(f"{var_name} = {result}")

    # -----------------------------------------
    # Handle: PRINT expr
    # -----------------------------------------
    def handle_print(self):
        self.advance()  # skip PRINT

        result = self.parse_expression()

        self.code.append(f"PRINT {result}")

    # -----------------------------------------
    # Expression Parsing (same logic as parser)
    # -----------------------------------------
    def parse_expression(self):
        left = self.parse_term()

        while True:
            token = self.current_token()

            if token and token.type == "OPERATOR" and token.value in {"+", "-"}:
                op = token.value
                self.advance()

                right = self.parse_term()

                temp = self.new_temp()
                self.code.append(f"{temp} = {left} {op} {right}")

                left = temp
            else:
                break

        return left

    def parse_term(self):
        left = self.parse_factor()

        while True:
            token = self.current_token()

            if token and token.type == "OPERATOR" and token.value in {"*", "/"}:
                op = token.value
                self.advance()

                right = self.parse_factor()

                temp = self.new_temp()
                self.code.append(f"{temp} = {left} {op} {right}")

                left = temp
            else:
                break

        return left

    def parse_factor(self):
        token = self.current_token()

        if token.type in {"IDENTIFIER", "NUMBER"}:
            value = token.value
            self.advance()
            return value

        raise Exception(f"TAC Error: Unexpected token '{token.value}'")