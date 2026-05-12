class Node:

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def print_ast(node, indent="", last=True):
    if node is None:
        return

    # connector symbols
    if indent == "":
        print(str(node.value))   # root
    else:
        print(indent + ("└── " if last else "├── ") + str(node.value))

    indent += "    " if last else "│   "

    children = []

    if node.left:
        children.append(node.left)
    if node.right:
        children.append(node.right)

    for i, child in enumerate(children):
        print_ast(child, indent, i == len(children) - 1)


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, expected=None):
        tok = self.current()

        if tok is None:
            raise Exception("Unexpected end of input")

        if expected and tok[1] != expected:
            raise Exception(f"Expected '{expected}' at {tok[2]}")

        self.pos += 1
        return tok

    # E → T (+ T)*
    def parse_E(self):
        node = self.parse_T()

        while self.current() and self.current()[1] == '+':
            self.eat('+')
            node = Node('+', node, self.parse_T())

        return node

    # T → F (* F)*
    def parse_T(self):
        node = self.parse_F()

        while self.current() and self.current()[1] == '*':
            self.eat('*')
            node = Node('*', node, self.parse_F())

        return node

    # F → (E) | id | num
    def parse_F(self):
        tok = self.current()

        if tok is None:
            raise Exception("Unexpected end of input")

        # parentheses
        if tok[1] == '(':
            self.eat('(')
            node = self.parse_E()
            self.eat(')')
            return node

        # numbers or identifiers
        if tok[0] in ('NUMBER', 'FLOAT', 'IDENTIFIER'):
            self.eat()
            return Node(tok[1])

        raise Exception(f"Syntax error at {tok}")
