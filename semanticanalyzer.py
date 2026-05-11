# AST NODES


class ASTNode:
    pass


class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class VarDecl(ASTNode):
    def __init__(self, name, var_type, value=None):
        self.name = name
        self.var_type = var_type
        self.value = value


class Assign(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Var(ASTNode):
    def __init__(self, name):
        self.name = name


class IntLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class FloatLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class BoolLiteral(ASTNode):
    def __init__(self, value):
        self.value = value



# SYMBOL TABLE


class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def insert(self, name, var_type):
        if name in self.symbols:
            return f"Semantic Error: variable '{name}' already declared"

        self.symbols[name] = var_type
        return None

    def lookup(self, name):
        return self.symbols.get(name)

    def display(self):
        print("\n==============================")
        print(" SYMBOL TABLE")
        print("==============================")

        if not self.symbols:
            print("No symbols declared.")
            return

        for name, var_type in self.symbols.items():
            print(f"{name} : {var_type}")



# SEMANTIC ANALYZER


class SemanticAnalyzer:
    def __init__(self, trace=True):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.trace = trace
        self.indent = 0

    def log(self, message):
        if self.trace:
            print("  " * self.indent + message)

    def add_error(self, message):
        self.errors.append(message)
        self.log(message)

    def analyze(self, program):
        self.log("==============================")
        self.log(" STARTING SEMANTIC ANALYSIS")
        self.log("==============================")

        self.visit(program)

        self.symbol_table.display()

        print("\n==============================")
        print(" SEMANTIC ANALYSIS RESULT")
        print("==============================")

        if len(self.errors) == 0:
            print("Semantic Analysis Passed")
        else:
            print("Semantic Analysis Failed")
            print("\nErrors Found:")
            for error in self.errors:
                print("-", error)

    def visit(self, node):
        if isinstance(node, Program):
            return self.visit_program(node)

        elif isinstance(node, VarDecl):
            return self.visit_var_decl(node)

        elif isinstance(node, Assign):
            return self.visit_assign(node)

        elif isinstance(node, BinOp):
            return self.visit_bin_op(node)

        elif isinstance(node, Var):
            return self.visit_var(node)

        elif isinstance(node, IntLiteral):
            self.log(f"Integer literal '{node.value}' has type int")
            return "int"

        elif isinstance(node, FloatLiteral):
            self.log(f"Float literal '{node.value}' has type float")
            return "float"

        elif isinstance(node, StringLiteral):
            self.log(f"String literal '{node.value}' has type string")
            return "string"

        elif isinstance(node, BoolLiteral):
            self.log(f"Boolean literal '{node.value}' has type bool")
            return "bool"

        else:
            self.add_error(f"Semantic Error: unknown AST node '{type(node).__name__}'")
            return "error"

    def visit_program(self, node):
        self.log(f"Program contains {len(node.statements)} statements")

        for index, statement in enumerate(node.statements, start=1):
            print()
            self.log(f"Statement {index}: {type(statement).__name__}")
            self.indent += 1
            self.visit(statement)
            self.indent -= 1

    def visit_var_decl(self, node):
        allowed_types = ["int", "float", "string", "bool"]

        self.log(f"Checking declaration: {node.var_type} {node.name}")

        if node.var_type not in allowed_types:
            self.add_error(
                f"Semantic Error: unknown type '{node.var_type}' for variable '{node.name}'"
            )
            return "error"

        error = self.symbol_table.insert(node.name, node.var_type)

        if error:
            self.add_error(error)
            return "error"

        self.log(f"Declared variable '{node.name}' with type '{node.var_type}'")

        if node.value is not None:
            self.log(f"Checking initialization value for '{node.name}'")
            self.indent += 1
            value_type = self.visit(node.value)
            self.indent -= 1

            if value_type != "error" and value_type != node.var_type:
                self.add_error(
                    f"Type Error: cannot initialize '{node.name}' of type "
                    f"{node.var_type} with value of type {value_type}"
                )
                return "error"

        return node.var_type

    def visit_assign(self, node):
        self.log(f"Checking assignment to variable '{node.name}'")

        variable_type = self.symbol_table.lookup(node.name)

        if variable_type is None:
            self.add_error(f"Semantic Error: variable '{node.name}' is not declared")
            return "error"

        self.log(f"Variable '{node.name}' found with type '{variable_type}'")

        self.log("Checking right-hand-side expression")
        self.indent += 1
        expression_type = self.visit(node.expr)
        self.indent -= 1

        if expression_type == "error":
            return "error"

        if variable_type != expression_type:
            self.add_error(
                f"Type Error: cannot assign {expression_type} value to "
                f"'{node.name}' of type {variable_type}"
            )
            return "error"

        self.log("Assignment is valid")
        return variable_type

    def visit_bin_op(self, node):
        self.log(f"Checking binary operation '{node.op}'")

        self.log("Checking left operand")
        self.indent += 1
        left_type = self.visit(node.left)
        self.indent -= 1

        self.log("Checking right operand")
        self.indent += 1
        right_type = self.visit(node.right)
        self.indent -= 1

        if left_type == "error" or right_type == "error":
            return "error"

        arithmetic_ops = ["+", "-", "*", "/"]
        relational_ops = ["<", ">", "<=", ">=", "==", "!="]

        if node.op in arithmetic_ops:
            if left_type not in ["int", "float"] or right_type not in ["int", "float"]:
                self.add_error(
                    f"Type Error: operator '{node.op}' cannot be applied to "
                    f"{left_type} and {right_type}"
                )
                return "error"

            if left_type == "float" or right_type == "float":
                self.log("Arithmetic operation returns float")
                return "float"

            self.log("Arithmetic operation returns int")
            return "int"

        elif node.op in relational_ops:
            if left_type != right_type:
                self.add_error(
                    f"Type Error: relational operator '{node.op}' requires matching types, "
                    f"got {left_type} and {right_type}"
                )
                return "error"

            self.log("Relational operation returns bool")
            return "bool"

        else:
            self.add_error(f"Semantic Error: unsupported operator '{node.op}'")
            return "error"

    def visit_var(self, node):
        self.log(f"Checking variable usage '{node.name}'")

        variable_type = self.symbol_table.lookup(node.name)

        if variable_type is None:
            self.add_error(f"Semantic Error: variable '{node.name}' is not declared")
            return "error"

        self.log(f"Variable '{node.name}' has type '{variable_type}'")
        return variable_type



# TEST PROGRAM


if __name__ == "__main__":
    program = Program([
        VarDecl("x", "int", IntLiteral(10)),
        VarDecl("y", "int", IntLiteral(20)),
        VarDecl("z", "int"),

        Assign("z", BinOp(Var("x"), "+", Var("y"))),

        VarDecl("name", "string", StringLiteral("Compiler")),
        Assign("name", IntLiteral(100)),

        Assign("unknown", IntLiteral(5)),

        VarDecl("x", "float", FloatLiteral(3.5)),

        VarDecl("flag", "bool"),
        Assign("flag", BinOp(Var("x"), ">", Var("y"))),
    ])

    analyzer = SemanticAnalyzer(trace=True)
    analyzer.analyze(program)