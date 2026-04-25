# =========================================================
# AST NODE
# =========================================================

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# =========================================================
# SEMANTIC ANALYZER
# =========================================================

class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast

    # -------------------------------------------------
    # Recursive type checking
    # -------------------------------------------------
    def check(self, node):

        if node is None:
            return None

        # -------------------------------------------------
        # Leaf node (must be integer)
        # -------------------------------------------------
        if node.left is None and node.right is None:

            if isinstance(node.value, int) or str(node.value).isdigit():
                return "int"

            raise Exception(f"Semantic Error: Invalid token '{node.value}'")

        # -------------------------------------------------
        # Evaluate left and right subtree
        # -------------------------------------------------
        left_type = self.check(node.left)
        right_type = self.check(node.right)

        # -------------------------------------------------
        # Operator checking
        # -------------------------------------------------
        if node.value in ['+', '-', '*', '/']:

            if left_type != "int" or right_type != "int":
                raise Exception(
                    f"Type Error: Cannot apply '{node.value}' to {left_type} and {right_type}"
                )

            return "int"

        raise Exception(f"Unknown operator: {node.value}")

    # -------------------------------------------------
    # Run semantic analysis
    # -------------------------------------------------
    def analyze(self):
        result_type = self.check(self.ast)

        print("\n==============================")
        print(" SEMANTIC ANALYSIS PASSED ✔")
        print("==============================")
        print("Expression Type:", result_type)


# =========================================================
# TEST AST (example expression)
# =========================================================
# Expression: 10 + 20 * (30 + 5)

ast = Node("+",
           Node(10),
           Node("*",
                Node(20),
                Node("+",
                     Node(30),
                     Node(5)
                )
           )
)


# =========================================================
# RUN ANALYZER
# =========================================================

analyzer = SemanticAnalyzer(ast)
analyzer.analyze()