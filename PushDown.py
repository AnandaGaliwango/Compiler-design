class PDA:
    def __init__(self, tokens):
        self.tokens = tokens
        self.stack = []

    # ----------------------------------------
    # SHIFT (push input to stack)
    # ----------------------------------------
    def shift(self, token):
        self.stack.append(token)
        print("SHIFT :", self.stack)

    # ----------------------------------------
    # REDUCE rules (grammar → stack actions)
    # ----------------------------------------
    def reduce(self):
        changed = True

        while changed:
            changed = False

            # F → id
            for i in range(len(self.stack)):
                if self.stack[i] == ('IDENTIFIER', 'id'):
                    self.stack[i] = 'F'
                    print("REDUCE: id → F")
                    changed = True
                    break

                if isinstance(self.stack[i], tuple) and self.stack[i][0] in ('IDENTIFIER', 'NUMBER'):
                    self.stack[i] = 'F'
                    print(f"REDUCE: {self.stack[i]} → F")
                    changed = True
                    break

            # (E) → F
            for i in range(len(self.stack) - 2):
                if self.stack[i] == '(' and self.stack[i+1] == 'E' and self.stack[i+2] == ')':
                    self.stack[i:i+3] = ['F']
                    print("REDUCE: (E) → F")
                    changed = True
                    break

            # F * F → T
            for i in range(len(self.stack) - 2):
                if self.stack[i] == 'F' and self.stack[i+1] == '*' and self.stack[i+2] == 'F':
                    self.stack[i:i+3] = ['T']
                    print("REDUCE: F * F → T")
                    changed = True
                    break

            # F + F → E
            for i in range(len(self.stack) - 2):
                if self.stack[i] == 'F' and self.stack[i+1] == '+' and self.stack[i+2] == 'F':
                    self.stack[i:i+3] = ['E']
                    print("REDUCE: F + F → E")
                    changed = True
                    break

    # ----------------------------------------
    # MAIN PROCESS
    # ----------------------------------------
    def parse(self):
        for token in self.tokens:
            self.shift(token)
            self.reduce()

        self.reduce()

        print("\nFINAL STACK:", self.stack)


# =========================================================
# TEST INPUT (from lexer)
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

pda = PDA(tokens)
pda.parse()