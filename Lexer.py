import re

token_specification = [

    ('FLOAT', r'\d+\.\d+'),
    ('NUMBER', r'\d+'),
    ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),

    ('OPERATOR', r'[+\-*/]'),
    ('SEPARATOR', r'[()]'),

    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.'),
]

token_regex = '|'.join(
    f'(?P<{name}>{pattern})'
    for name, pattern in token_specification
)

def lexer(code):
    tokens = []

    for match in re.finditer(token_regex, code):

        kind = match.lastgroup
        value = match.group()
        pos = match.start()

        if kind == 'SKIP':
            continue

        if kind == 'MISMATCH':
            raise Exception(f"Lexical error: Illegal character '{value}' at {pos}")

        tokens.append((kind, value, pos))

    return tokens
