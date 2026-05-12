class SemanticAnalyzer:

    def __init__(self):
        # variable types (unknown by default)
        self.symbol_table = set()

    def visit(self, node):

        if node is None:
            return None

        # -------------------------
        # LEAF NODE
        # -------------------------
        if node.left is None and node.right is None:

            # number literal
            if node.value.replace('.', '', 1).isdigit():
                return "NUMBER"

            # identifier (VARIABLE)
            if node.value.isidentifier():
                return "IDENTIFIER"

        # -------------------------
        # BINARY OPERATION
        # -------------------------
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.value in ['+', '-', '*', '/']:

            # STRICT RULES (THIS IS WHAT YOU WANT)
            if left != "NUMBER" or right != "NUMBER":
                raise Exception(
                    f"Type Error: cannot apply '{node.value}' "
                    f"between {left} and {right}"
                )

            return "NUMBER"

        return None
