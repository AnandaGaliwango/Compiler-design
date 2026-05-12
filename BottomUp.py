class ShiftReduceParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.stack = []

    # -----------------------------------------
    # Utility: print stack nicely
    # -----------------------------------------
    def stack_view(self):
        def fmt(x):
            if isinstance(x, tuple):
                return x[1]
            return str(x)
        return " ".join(fmt(s) for s in self.stack)

    # -----------------------------------------
    # SHIFT operation
    # -----------------------------------------
    def shift(self, token):
        self.stack.append(token)
        print(f"SHIFT  : {self.stack_view()}")

    # -----------------------------------------
    # REDUCTION rules
    # -----------------------------------------
    def reduce(self):
        changed = True

        while changed:
            changed = False

            # -------------------------
            # id / num → F
            # -------------------------
            for i in range(len(self.stack)):
                if isinstance(self.stack[i], tuple):
                    if self.stack[i][0] in ('IDENTIFIER', 'NUMBER'):
                        print(f"REDUCE : {self.stack[i][1]} → F")

                        self.stack[i] = 'F'
                        changed = True
                        break

            # -------------------------
            # (F) → F
            # -------------------------
            for i in range(len(self.stack) - 2):
                if self.stack[i] == '(' and self.stack[i+1] == 'F' and self.stack[i+2] == ')':
                    print("REDUCE : (F) → F")

                    self.stack[i:i+3] = ['F']
                    changed = True
                    break

            # -------------------------
            # F * F → F
            # -------------------------
            for i in range(len(self.stack) - 2):
                if self.stack[i] == 'F' and self.stack[i+1] == '*' and self.stack[i+2] == 'F':
                    print("REDUCE : F * F → F")

                    self.stack[i:i+3] = ['F']
                    changed = True
                    break

            # -------------------------
            # F + F → F
            # -------------------------
            for i in range(len(self.stack) - 2):
                if self.stack[i] == 'F' and self.stack[i+1] == '+' and self.stack[i+2] == 'F':
                    print("REDUCE : F + F → F")

                    self.stack[i:i+3] = ['F']
                    changed = True
                    break

    # -----------------------------------------
    # MAIN PARSE LOOP
    # -----------------------------------------
    def parse(self):
        for token in self.tokens:
            self.shift(token)
            self.reduce()

        # final reductions
        self.reduce()

        print("\nFINAL STACK:", self.stack)


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
# RUN
# =========================================================

parser = ShiftReduceParser(tokens)
parser.parse()
