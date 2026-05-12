# =========================================================
# AST NODE
# =========================================================

class Node:

    def __init__(self, value, left=None, right=None):

        self.value = value

        self.left = left

        self.right = right


# =========================================================
# PRINT AST
# =========================================================

def print_ast(node, level=0):

    if node:

        print("   " * level + str(node.value))

        print_ast(node.left, level + 1)

        print_ast(node.right, level + 1)


# =========================================================
# PARSER
# =========================================================

class Parser:

    def __init__(self, tokens):

        self.tokens = tokens

        self.pos = 0


    # =====================================================
    # CURRENT TOKEN
    # =====================================================

    def current(self):

        if self.pos < len(self.tokens):

            return self.tokens[self.pos]

        return None


    # =====================================================
    # EAT TOKEN
    # =====================================================

    def eat(self, expected=None):

        tok = self.current()

        if tok is None:

            raise Exception("Unexpected end of input")

        if expected and tok[1] != expected:

            raise Exception(

                f"Expected '{expected}' "

                f"but found '{tok[1]}' "

                f"at position {tok[2]}"
            )

        self.pos += 1

        return tok


    # =====================================================
    # E → T (+ T)*
    # =====================================================

    def parse_E(self):

        node = self.parse_T()

        while self.current() and self.current()[1] == '+':

            self.eat('+')

            node = Node('+', node, self.parse_T())

        return node


    # =====================================================
    # T → F (* F)*
    # =====================================================

    def parse_T(self):

        node = self.parse_F()

        while self.current() and self.current()[1] == '*':

            self.eat('*')

            node = Node('*', node, self.parse_F())

        return node


    # =====================================================
    # F → (E) | id | num
    # =====================================================

    def parse_F(self):

        tok = self.current()

        if tok is None:

            raise Exception("Unexpected end of input")


        # (E)
        if tok[1] == '(':

            self.eat('(')

            node = self.parse_E()

            self.eat(')')

            return node


        # IDENTIFIER / NUMBER
        elif tok[0] in ('IDENTIFIER', 'NUMBER', 'FLOAT'):

            self.eat()

            return Node(tok[1])


        else:

            raise Exception(

                f"Unexpected token '{tok[1]}' "

                f"at position {tok[2]}"
            )