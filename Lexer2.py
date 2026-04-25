import re

token_specification = [
    ('FLOAT', r'[0-9]+\.[0-9]+'),
    ('BOOLEAN', r'\b(true|false)\b'),
    ('COMMENT', r'//.*'),
    ('UG_PHONE', r'(\+256|0)[0-9]{9}'),
    ('NUMBER',   r'[0-9]+'),
    ('KEYWORD', r'\b(int|float|if|else|while|return)\b'),
    ('IDENTIFIER', r'[A-Za-z][A-Za-z0-9]*'),
    ('RELATIONAL', r'==|!=|<=|>=|<|>'),
    ('OPERATOR', r'[\+\-\*/=]'),
    ('SEPARATOR', r'[(),;]'),
    ('STRING', r'"[^"]*"|\'[^\']*\''),
    ('SKIP', r'[ \t]+'),

]

token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

def lexer(code):
    tokens = []
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()

        if kind == 'SKIP':
            continue

        tokens.append((kind, value))

    return tokens

code = "x + y * (z + 5)"

print(lexer(code))