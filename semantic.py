# =========================================================
# SEMANTIC ANALYZER
# =========================================================

class SemanticAnalyzer:

    def __init__(self):

        # store declared variables
        self.symbol_table = set()


    # =====================================================
    # visit AST
    # =====================================================

    def visit(self, node):

        if node is None:
            return


        # leaf node (number or variable)
        if node.left is None and node.right is None:

            # if it's a number → OK
            if node.value.replace('.', '', 1).isdigit():

                return "NUMBER"


            # variable
            if node.value.isidentifier():

                if node.value not in self.symbol_table:

                    raise Exception(
                        f"Semantic Error: variable '{node.value}' is not defined"
                    )

                return "IDENTIFIER"


        # binary operation
        left_type = self.visit(node.left)

        right_type = self.visit(node.right)


        # type checking rules (simple)
        if node.value in ['+', '-', '*', '/']:

            if left_type != right_type:

                raise Exception(
                    f"Type Error: cannot apply '{node.value}' "
                    f"between {left_type} and {right_type}"
                )

            return left_type


        return None