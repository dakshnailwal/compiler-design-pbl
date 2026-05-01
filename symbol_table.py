# symbol_table.py

# -----------------------------------------
# Symbol Table Class
# -----------------------------------------

class SymbolTable:
    def __init__(self):
        # Stores variables like:
        # { "a": {"type": "int"} }
        self.table = {}

    # -----------------------------------------
    # Insert variable
    # -----------------------------------------
    def insert(self, name):
        if name in self.table:
            raise Exception(f"Semantic Error: Variable '{name}' already declared")

        self.table[name] = {"type": "int"}

    # -----------------------------------------
    # Lookup variable
    # -----------------------------------------
    def lookup(self, name):
        if name not in self.table:
            raise Exception(f"Semantic Error: Variable '{name}' not declared")

        return self.table[name]

    # -----------------------------------------
    # Display table (clean format)
    # -----------------------------------------
    def display(self):
        print("\nSYMBOL TABLE:")
        print("---------------------------------")
        print("Name  | Type")
        print("----------------")

        # 🔹 FIX: This loop must be INSIDE the function
        for var, info in self.table.items():
            print(f"{var:<5} | {info['type']}")