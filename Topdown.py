# =========================================================
# AST NODE
# =========================================================

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# =========================================================
# TOP-DOWN RECURSIVE DESCENT PARSER
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

    # -------------------------------------------------
    # E → T (+ T)*
    # -------------------------------------------------
    def parse_E(self):
        node = self.parse_T()

        while self.current() and self.current()[1] == '+':
            self.eat()  # consume '+'
            node = Node('+', node, self.parse_T())

        return node

    # -------------------------------------------------
    # T → F (* F)*
    # -------------------------------------------------
    def parse_T(self):
        node = self.parse_F()

        while self.current() and self.current()[1] == '*':
            self.eat()  # consume '*'
            node = Node('*', node, self.parse_F())

        return node

    # -------------------------------------------------
    # F → (E) | id | num
    # -------------------------------------------------
    def parse_F(self):
        tok = self.current()

        if tok is None:
            raise Exception("Unexpected end of input")

        # (E)
        if tok[1] == '(':
            self.eat()
            node = self.parse_E()

            if self.current() and self.current()[1] == ')':
                self.eat()
                return node
            else:
                raise Exception("Missing closing parenthesis")

        # id or num
        elif tok[0] in ('IDENTIFIER', 'NUMBER'):
            self.eat()
            return Node(tok[1])

        else:
            raise Exception(f"Syntax error at {tok}")


# =========================================================
# AST PRINTING
# =========================================================

def print_ast(node, level=0):
    if node:
        print("  " * level + str(node.value))
        print_ast(node.left, level + 1)
        print_ast(node.right, level + 1)


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
# RUN PARSER
# =========================================================

parser = Parser(tokens)
ast = parser.parse_E()

print("=== TOP-DOWN PARSING (RECURSIVE DESCENT) ===")
print_ast(ast)