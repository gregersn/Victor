from .tokens import Token

RESERVED_KEYWORDS = {
    'if': Token('RESERVED', 'IF'),
    'elif': Token('RESERVED', 'ELIF'),
    'then': Token('RESERVED', 'THEN'),
    'else': Token('RESERVED', 'ELSE'),
    'and': Token('RESERVED', 'AND'),
    'or': Token('RESERVED', 'OR'),
    'max': Token('RESERVED', 'MAX')
}

SYSTEM_KEYWORDS = {
    'sum': Token('SYSTEM', 'SUM')
}
