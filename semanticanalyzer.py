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


class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class BoolLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


# SYMBOL TABLE


class SymbolTable:
    def __init__(self):
        self.scopes = [{}]

    def insert(self, name, var_type):
        current_scope = self.scopes[-1]

        if name in current_scope:
            return f"Variable '{name}' already declared in this scope"

        current_scope[name] = var_type
        return None

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]

        return None

    def show(self):
        return self.scopes


# SEMANTIC ANALYZER WITH TRACE OUTPUT

class SemanticAnalyzer:
    def __init__(self, trace=True):
        self.symtab = SymbolTable()
        self.errors = []
        self.trace = trace
        self.indent = 0

    def log(self, message):
        if self.trace:
            print("  " * self.indent + message)

    def error(self, message):
        self.errors.append(message)
        self.log(f"ERROR: {message}")

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
            self.log(f"Integer literal {node.value} has type int")
            return "int"

        elif isinstance(node, StringLiteral):
            self.log(f"String literal '{node.value}' has type string")
            return "string"

        elif isinstance(node, BoolLiteral):
            self.log(f"Boolean literal {node.value} has type bool")
            return "bool"

        else:
            self.error(f"Unknown AST node: {type(node).__name__}")
            return "error"

    def visit_program(self, node):
        self.log("Starting semantic analysis...")
        self.log(f"Program has {len(node.statements)} statements")
        print()

        for index, statement in enumerate(node.statements, start=1):
            self.log(f"Statement {index}: {type(statement).__name__}")
            self.indent += 1
            self.visit(statement)
            self.indent -= 1
            self.log(f"Symbol table now: {self.symtab.show()}")
            print()

    def visit_var_decl(self, node):
        self.log(f"Checking variable declaration: {node.var_type} {node.name}")

        allowed_types = ["int", "string", "bool"]

        if node.var_type not in allowed_types:
            self.error(f"Unknown type '{node.var_type}' for variable '{node.name}'")
            return "error"

        self.log(f"Checking if '{node.name}' is already declared")
        err = self.symtab.insert(node.name, node.var_type)

        if err:
            self.error(err)
            return "error"

        self.log(f"Inserted '{node.name}' with type '{node.var_type}' into symbol table")

        if node.value is not None:
            self.log(f"Checking initialization value for '{node.name}'")
            self.indent += 1
            value_type = self.visit(node.value)
            self.indent -= 1

            self.log(f"Declared type: {node.var_type}, value type: {value_type}")

            if value_type != "error" and value_type != node.var_type:
                self.error(
                    f"Type mismatch in declaration of '{node.name}': "
                    f"expected {node.var_type}, got {value_type}"
                )
                return "error"

        return node.var_type

    def visit_assign(self, node):
        self.log(f"Checking assignment to variable '{node.name}'")

        self.log(f"Looking up '{node.name}' in symbol table")
        var_type = self.symtab.lookup(node.name)

        if var_type is None:
            self.error(f"Undeclared variable '{node.name}'")
            return "error"

        self.log(f"Variable '{node.name}' found with type '{var_type}'")

        self.log(f"Checking right-hand side expression")
        self.indent += 1
        expr_type = self.visit(node.expr)
        self.indent -= 1

        self.log(f"Left type: {var_type}, right type: {expr_type}")

        if expr_type == "error":
            return "error"

        if var_type != expr_type:
            self.error(
                f"Type mismatch: cannot assign {expr_type} to variable "
                f"'{node.name}' of type {var_type}"
            )
            return "error"

        self.log("Assignment is semantically valid")
        return var_type

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

        self.log(f"Left operand type: {left_type}")
        self.log(f"Right operand type: {right_type}")

        if left_type == "error" or right_type == "error":
            return "error"

        arithmetic_ops = ["+", "-", "*", "/"]
        comparison_ops = ["<", ">", "<=", ">=", "==", "!="]
        logical_ops = ["&&", "||"]

        if node.op in arithmetic_ops:
            self.log(f"Operator '{node.op}' is arithmetic, so both operands must be int")

            if left_type != "int" or right_type != "int":
                self.error(
                    f"Arithmetic operator '{node.op}' requires int operands, "
                    f"got {left_type} and {right_type}"
                )
                return "error"

            self.log("Binary operation is valid and returns int")
            return "int"

        elif node.op in comparison_ops:
            self.log(f"Operator '{node.op}' is comparison, result type will be bool")

            if left_type != right_type:
                self.error(
                    f"Comparison operator '{node.op}' requires operands of same type, "
                    f"got {left_type} and {right_type}"
                )
                return "error"

            self.log("Binary operation is valid and returns bool")
            return "bool"

        elif node.op in logical_ops:
            self.log(f"Operator '{node.op}' is logical, so both operands must be bool")

            if left_type != "bool" or right_type != "bool":
                self.error(
                    f"Logical operator '{node.op}' requires bool operands, "
                    f"got {left_type} and {right_type}"
                )
                return "error"

            self.log("Binary operation is valid and returns bool")
            return "bool"

        else:
            self.error(f"Unsupported binary operator '{node.op}'")
            return "error"

    def visit_var(self, node):
        self.log(f"Checking variable usage: '{node.name}'")

        var_type = self.symtab.lookup(node.name)

        if var_type is None:
            self.error(f"Undeclared variable '{node.name}'")
            return "error"

        self.log(f"Variable '{node.name}' has type {var_type}")
        return var_type


# TEST PROGRAM


program = Program([
    VarDecl("x", "int"),
    VarDecl("x", "int"),                    # Error: redeclaration

    Assign("x", IntLiteral(5)),             # OK

    Assign("y", IntLiteral(10)),            # Error: y not declared

    VarDecl("z", "int"),
    Assign("z", BinOp(Var("x"), "+", IntLiteral(3))),  # OK
    Assign("z", BinOp(Var("x"), "+", Var("z"))),       # OK

    VarDecl("name", "string", StringLiteral("Salimu")),  # OK
    Assign("name", IntLiteral(20)),                     # Error: int to string

    VarDecl("flag", "bool", BoolLiteral(True)),          # OK
    Assign("flag", BinOp(Var("x"), ">", IntLiteral(2))), # OK

    Assign("z", BinOp(Var("name"), "+", IntLiteral(3))), # Error: string + int
])


analyzer = SemanticAnalyzer(trace=True)
analyzer.visit(program)

print("FINAL SEMANTIC ERRORS:")

if not analyzer.errors:
    print("No semantic errors found.")
else:
    for err in analyzer.errors:
        print("-", err)