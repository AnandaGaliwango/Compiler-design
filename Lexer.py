class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.length = len(source_code)

        self.keywords = {"int", "float", "if", "else", "while", "return", "if else"}
        self.separators = {';', ',', '(', ')', '{', '}'}
        self.single_operators = {'+', '-', '*', '/', '=', '<', '>'}
        self.double_operators = {'==', '!=', '<=', '>='}

    def peek(self):
        if self.position < self.length:
            return self.source[self.position]
        return None

    def advance(self):
        char = self.peek()
        self.position += 1
        return char

    def tokenize(self):
        tokens = []

        while self.position < self.length:
            current = self.peek()

            # Skip whitespace
            if current.isspace():
                self.advance()
                continue

            # Identifier or keyword
            if current.isalpha() or current == '_':
                token = self.read_identifier()
                if token in self.keywords:
                    tokens.append(("KEYWORD", token))
                else:
                    tokens.append(("IDENTIFIER", token))
                continue

            # Number
            if current.isdigit():
                token = self.read_number()
                tokens.append(("NUMBER", token))
                continue

            # Two-character operators
            two_char = self.source[self.position:self.position + 2]
            if two_char in self.double_operators:
                tokens.append(("OPERATOR", two_char))
                self.position += 2
                continue

            # Single-character operators
            if current in self.single_operators:
                tokens.append(("OPERATOR", current))
                self.advance()
                continue

            # Separators
            if current in self.separators:
                tokens.append(("SEPARATOR", current))
                self.advance()
                continue

            # Unknown character
            tokens.append(("UNKNOWN", current))
            self.advance()

        return tokens

    def read_identifier(self):
        start = self.position
        while self.peek() is not None and (self.peek().isalnum() or self.peek() == '_'):
            self.advance()
        return self.source[start:self.position]

    def read_number(self):
        start = self.position
        while self.peek() is not None and self.peek().isdigit():
            self.advance()
        return self.source[start:self.position]


# Test input
source_code = """
int a = 5;
if (a >= 3) {
    a = a + 1;
}
"""

lexer = Lexer(source_code)
tokens = lexer.tokenize()

for token in tokens:
    print(token)