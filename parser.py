# parser.py

# -----------------------------------------
# Parser Class
# -----------------------------------------

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # -----------------------------------------
    # Get current token
    # -----------------------------------------
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    # -----------------------------------------
    # Move to next token
    # -----------------------------------------
    def advance(self):
        self.pos += 1

    # -----------------------------------------
    # Match expected token
    # -----------------------------------------
    def expect(self, type_, value=None):
        token = self.current_token()

        if token is None:
            raise Exception("Syntax Error: Unexpected end of input")

        if token.type != type_:
            raise Exception(f"Syntax Error: Expected {type_}, got {token.type}")

        if value and token.value != value:
            raise Exception(f"Syntax Error: Expected '{value}', got '{token.value}'")

        self.advance()

    # -----------------------------------------
    # PROGRAM → START stmt_list END
    # -----------------------------------------
    def parse_program(self):
        self.expect("KEYWORD", "START")

        self.parse_stmt_list()

        self.expect("KEYWORD", "END")

        if self.current_token() is not None:
            raise Exception("Syntax Error: Unexpected tokens after END")

    # -----------------------------------------
    # stmt_list → stmt stmt_list | ε
    # -----------------------------------------
    def parse_stmt_list(self):
        while True:
            token = self.current_token()

            if token is None:
                break

            if token.type == "KEYWORD" and token.value == "END":
                break

            self.parse_stmt()

    # -----------------------------------------
    # stmt → decl_stmt | print_stmt
    # -----------------------------------------
    def parse_stmt(self):
        token = self.current_token()

        if token.type == "KEYWORD" and token.value == "INT":
            self.parse_decl()

        elif token.type == "KEYWORD" and token.value == "PRINT":
            self.parse_print()

        else:
            raise Exception(f"Syntax Error: Unexpected token '{token.value}'")

    # -----------------------------------------
    # decl_stmt → INT id = expr
    # -----------------------------------------
    def parse_decl(self):
        self.expect("KEYWORD", "INT")
        self.expect("IDENTIFIER")
        self.expect("ASSIGN")

        self.parse_expr()   # now supports full expression

    # -----------------------------------------
    # print_stmt → PRINT expr
    # -----------------------------------------
    def parse_print(self):
        self.expect("KEYWORD", "PRINT")

        self.parse_expr()   # now supports full expression

    # -----------------------------------------
    # expr → term ((+ | -) term)*
    # -----------------------------------------
    def parse_expr(self):
        self.parse_term()

        while True:
            token = self.current_token()

            if token and token.type == "OPERATOR" and token.value in {"+", "-"}:
                self.advance()
                self.parse_term()
            else:
                break

    # -----------------------------------------
    # term → factor ((* | /) factor)*
    # -----------------------------------------
    def parse_term(self):
        self.parse_factor()

        while True:
            token = self.current_token()

            if token and token.type == "OPERATOR" and token.value in {"*", "/"}:
                self.advance()
                self.parse_factor()
            else:
                break

    # -----------------------------------------
    # factor → IDENTIFIER | NUMBER
    # -----------------------------------------
    def parse_factor(self):
        token = self.current_token()

        if token is None:
            raise Exception("Syntax Error: Unexpected end of input")

        if token.type in {"IDENTIFIER", "NUMBER"}:
            self.advance()
        else:
            raise Exception(f"Syntax Error: Unexpected token '{token.value}'")