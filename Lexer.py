import re

# =========================================================
# TOKEN DEFINITIONS
# =========================================================

token_specification = [


    ('FLOAT', r'[0-9]+\.[0-9]+'),

    ('NUMBER', r'[0-9]+'),

    ('IDENTIFIER', r'[A-Za-z][A-Za-z0-9]*'),

    ('RELATIONAL', r'==|!=|<=|>=|<|>'),

    ('OPERATOR', r'[\+\-\*/=]'),

    ('SEPARATOR', r'[(),;]'),

    ('SKIP', r'[ \t]+'),

    ('MISMATCH', r'.'),
]


# =========================================================
# BUILD REGEX
# =========================================================

token_regex = '|'.join(

    f'(?P<{name}>{pattern})'

    for name, pattern in token_specification
)


# =========================================================
# LEXER
# =========================================================

def lexer(code):

    tokens = []

    for match in re.finditer(token_regex, code):

        kind = match.lastgroup

        value = match.group()

        position = match.start()

        # Ignore spaces
        if kind == 'SKIP':
            continue

        # Illegal character
        if kind == 'MISMATCH':

            raise Exception(

                f"Illegal character '{value}' "

                f"at position {position}"
            )

        tokens.append((kind, value, position))

    return tokens