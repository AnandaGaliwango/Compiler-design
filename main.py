# =========================================================
# AST NODE  
# =========================================================

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# =========================================================
# PARSER (AST BUILDER - SAME FOR BOTH)
# =========================================================


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self):
        tok = self.current()
        self.pos += 1
        return tok

    # E → T (+ T)*
    def parse_E(self):
        node = self.parse_T()

        while self.current() and self.current()[1] == '+':
            self.eat()
            node = Node('+', node, self.parse_T())

        return node

    # T → F (* F)*
    def parse_T(self):
        node = self.parse_F()

        while self.current() and self.current()[1] == '*':
            self.eat()
            node = Node('*', node, self.parse_F())

        return node

    # F → (E) | id | num
    def parse_F(self):
        tok = self.current()

        if tok[1] == '(':
            self.eat()
            node = self.parse_E()
            self.eat()  # ')'
            return node

        elif tok[0] in ('IDENTIFIER', 'NUMBER'):
            self.eat()
            return Node(tok[1])

        else:
            raise Exception("Syntax Error")


# =========================================================
# AST PRINTING
# =========================================================

def print_ast(node, level=0):
    if node:
        print("  " * level + str(node.value))
        print_ast(node.left, level + 1)
        print_ast(node.right, level + 1)


# =========================================================
# DERIVATION TRACER (LEFT OR RIGHT)
# =========================================================

def show_derivation(mode="left"):
    """
    mode = "left"  → leftmost derivation
    mode = "right" → rightmost derivation
    """

    if mode == "left":
        steps = [
            "E",
            "T + T",
            "F + T",
            "id + T",
            "id + T * F",
            "id + F * F",
            "id + id * F",
            "id + id * (E)",
            "id + id * (E + T)",
            "id + id * (T + T)",
            "id + id * (F + T)",
            "id + id * (id + T)",
            "id + id * (id + num)"
        ]

        print("\nLEFTMOST DERIVATION:")
        for s in steps:
            print("→", s)

    elif mode == "right":
        steps = [
            "E",
            "E + T",
            "E + T * F",
            "E + T * (E)",
            "E + T * (E + T)",
            "E + T * (E + num)",
            "E + T * (F + num)",
            "E + T * (id + num)",
            "E + F * (id + num)",
            "E + id * (id + num)",
            "T + id * (id + num)",
            "F + id * (id + num)",
            "id + id * (id + num)"
        ]

        print("\nRIGHTMOST DERIVATION:")
        for s in steps:
            print("→", s)

    else:
        print("Invalid mode. Use 'left' or 'right'.")


# =========================================================
# TEST INPUT (FROM YOUR LEXER)
# =========================================================

tokens = [
    ('IDENTIFIER', 'x'),
    ('OPERATOR', '+'),
    ('IDENTIFIER', 'y'),
    ('OPERATOR', '*'),
    ('SEPARATOR', '('),
    ('IDENTIFIER', 'z'),
    ('OPERATOR', '+'),
    ('NUMBER', '5'),
    ('SEPARATOR', ')')
]


# =========================================================
# RUN PROGRAM (CHOOSE MODE HERE)
# =========================================================

mode = input("Choose derivation (left/right): ").strip().lower()

parser = Parser(tokens)
ast = parser.parse_E()

print("\n=== ABSTRACT SYNTAX TREE ===")
print_ast(ast)

show_derivation(mode)
