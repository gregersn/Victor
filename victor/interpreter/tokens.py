from typing import Optional, Any
from .position import Position

ID = 'ID'
RESERVED = 'RESERVED'
SYSTEM = 'SYSTEM'
ASSIGN = 'ASSIGN'
REFERENCE = 'REFERENCE'

NUMBER = 'NUMBER'
STRING = 'STRING'
DIEROLL = 'DIEROLL'

MUL = 'MUL'
DIV = 'DIV'
IDIV = 'IDIV'
PLUS = 'PLUS'
MINUS = 'MINUS'

LPAREN = 'LPAREN'
RPAREN = 'RPAREN'

LESSTHAN = 'LESSTHAN'
GREATERTHAN = 'GREATERTHAN'

NEWLINE = 'NEWLINE'
COMMA = 'COMMA'
EOF = 'EOF'


class Token:
    pos_start: Optional[Position]
    pos_end: Optional[Position]
    _type: str
    _value: Any

    def __init__(self,
                 _type: str,
                 value: Any = None,
                 pos_start: Optional[Position] = None,
                 pos_end: Optional[Position] = None):
        self._type = _type
        self._value = value

        if pos_start is not None:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            if self.pos_end is not None:
                self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def __repr__(self) -> str:
        if self._value:
            return f"{self._type}: {self._value}"
        return f"{self._type}"

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    def matches(self, _type: str, value: Any = None) -> bool:
        return self._type == _type and self._value == value


class TokenDieRoll(Token):
    def __init__(self, _type: str, value: str):
        super(TokenDieRoll, self).__init__(_type, value)
