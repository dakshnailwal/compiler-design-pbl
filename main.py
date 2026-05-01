from lexer import tokenize
from parser import Parser
from semantic import SemanticAnalyzer
from intermediate_code import TACGenerator

def read_input():
    print("Enter your program (type END on a new line to finish):")

    lines = []
    while True:
        line = input()
        lines.append(line)

        if line.strip() == "END":
            break

    return "\n".join(lines)


def main():

    try:
        code = read_input()

        # LEXER
        tokens = tokenize(code)

        print("\nTOKENS:")
        print("---------------------------------")
        print(f"{'Value':<10} | Type")
        print("---------------------------")

        for token in tokens:
             print(token)

        # PARSER
        parser = Parser(tokens)
        parser.parse_program()
        print("\nSYNTAX: No errors found.")

        # SEMANTIC
        semantic = SemanticAnalyzer(tokens)
        semantic.analyze()
        semantic.symbol_table.display()

        # TAC
        tac = TACGenerator(tokens)
        code = tac.generate()

        print("\nINTERMEDIATE CODE:")
        print("---------------------------------")
        for line in code:
            print(line)

    except Exception as e:
        print("\nERROR:")
        print("---------------------------------")
        print(e)


if __name__ == "__main__":
    main()