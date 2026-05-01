# lexer.py

# -----------------------------------------
# TOKEN TYPES
# -----------------------------------------

KEYWORD = "KEYWORD"
IDENTIFIER = "IDENTIFIER"
NUMBER = "NUMBER"
OPERATOR = "OPERATOR"
ASSIGN = "ASSIGN"

# -----------------------------------------
# KEYWORDS
# -----------------------------------------

KEYWORDS = {"START", "END", "INT", "PRINT"}

# -----------------------------------------
# Token Class
# -----------------------------------------

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.value:<10} | {self.type}"


# -----------------------------------------
# LEXER FUNCTION (IMPROVED)
# -----------------------------------------

def tokenize(code):
    tokens = []
    i = 0
    length = len(code)

    while i < length:
        char = code[i]

        # ---------------------------------
        # Ignore whitespace
        # ---------------------------------
        if char.isspace():
            i += 1
            continue

        # ---------------------------------
        # IDENTIFIER or KEYWORD
        # starts with letter
        # ---------------------------------
        if char.isalpha():
            start = i
            while i < length and (code[i].isalnum()):
                i += 1

            word = code[start:i]

            if word in KEYWORDS:
                tokens.append(Token(KEYWORD, word))
            else:
                tokens.append(Token(IDENTIFIER, word))

            continue

        # ---------------------------------
        # NUMBER (only integers)
        # ---------------------------------
        if char.isdigit():
            start = i
            while i < length and code[i].isdigit():
                i += 1

            number = code[start:i]

            # check invalid like 12abc
            if i < length and code[i].isalpha():
                raise Exception(f"Lexical Error: Invalid identifier '{code[start:i+1]}'")

            tokens.append(Token(NUMBER, number))
            continue

        # ---------------------------------
        # OPERATORS
        # ---------------------------------
        if char in "+-*/":
            tokens.append(Token(OPERATOR, char))
            i += 1
            continue

        # ---------------------------------
        # ASSIGNMENT
        # ---------------------------------
        if char == "=":
            tokens.append(Token(ASSIGN, char))
            i += 1
            continue

        # ---------------------------------
        # INVALID CHARACTER
        # ---------------------------------
        raise Exception(f"Lexical Error: Invalid character '{char}'")

    return tokens