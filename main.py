from Lexer import lexer
from Parser import Parser, print_ast
from semantic import SemanticAnalyzer


code = input("Enter expression: ")

tokens = lexer(code)

parser = Parser(tokens)

ast = parser.parse_E()


# ensure full consumption
if parser.current() is not None:

    tok = parser.current()

    raise Exception(
        f"Unexpected token '{tok[1]}' at position {tok[2]}"
    )


print("\n=== AST ===")

print_ast(ast)


# =====================================================
# SEMANTIC ANALYSIS
# =====================================================

print("\n=== SEMANTIC ANALYSIS ===")
analyzer = SemanticAnalyzer()

# TEMPORARY FIX: predefined variables
analyzer.symbol_table = {"x", "y", "z"}


result_type = analyzer.visit(ast)

print("Semantic check passed. Expression type:", result_type)