from .tokens import Token

RESERVED_KEYWORDS = {
    'if': Token('RESERVED', 'IF'),
    'elif': Token('RESERVED', 'ELIF'),
    'then': Token('RESERVED', 'THEN'),
    'else': Token('RESERVED', 'ELSE'),
    'and': Token('RESERVED', 'AND'),
    'or': Token('RESERVED', 'OR'),
    'max': Token('RESERVED', 'MAX'),
    'choose': Token('RESERVED', 'CHOOSE'),
    'load_system': Token('RESERVED', 'LOAD_SYSTEM')
}
