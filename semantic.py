# semantic.py

from symbol_table import SymbolTable

# -----------------------------------------
# Semantic Analyzer
# -----------------------------------------

class SemanticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.symbol_table = SymbolTable()

    # -----------------------------------------
    # Helpers
    # -----------------------------------------
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        self.pos += 1

    # -----------------------------------------
    # PROGRAM → START stmt_list END
    # -----------------------------------------
    def analyze(self):
        while self.current_token() is not None:
            token = self.current_token()

            # Skip START and END
            if token.type == "KEYWORD" and token.value in {"START", "END"}:
                self.advance()

            elif token.type == "KEYWORD" and token.value == "INT":
                self.handle_declaration()

            elif token.type == "KEYWORD" and token.value == "PRINT":
                self.handle_print()

            else:
                self.advance()

    # -----------------------------------------
    # Handle declaration: INT a = expr
    # -----------------------------------------
    def handle_declaration(self):
        self.advance()  # skip INT

        # variable name
        var_token = self.current_token()
        var_name = var_token.value

        # insert into symbol table
        self.symbol_table.insert(var_name)

        self.advance()  # move past identifier

        self.advance()  # skip '='

        # check expression
        self.check_expression()

    # -----------------------------------------
    # Handle print: PRINT expr
    # -----------------------------------------
    def handle_print(self):
        self.advance()  # skip PRINT

        self.check_expression()

    # -----------------------------------------
    # Check expression tokens
    # -----------------------------------------
    def check_expression(self):
        while True:
            token = self.current_token()

            if token is None:
                break

            # stop at next statement
            if token.type == "KEYWORD":
                break

            if token.type == "IDENTIFIER":
                # ensure variable exists
                self.symbol_table.lookup(token.value)

            self.advance()