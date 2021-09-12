from .tokens import (Token, TokenDieRoll)
from .tokens import (STRING, DIEROLL, NUMBER,
                     REFERENCE, ID, PLUS, MINUS, MUL, IDIV, DIV,
                     LESSTHAN, GREATERTHAN, LPAREN, RPAREN,
                     ASSIGN, NEWLINE, COMMA, EOF)
from .keywords import RESERVED_KEYWORDS, SYSTEM_KEYWORDS
from typing import List, Optional
from .position import Position
from .error import IllegalCharError


class Tokenizer:
    _data: str
    pos: Position
    current_char: Optional[str]
    filename: str

    def __init__(self, data: str = ""):
        self.filename = ""
        self.program(data)

    def program(self, data: str):
        self._data = data
        self.pos = Position(-1, 0, -1, self.filename, self._data)
        self.current_char = None

        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        if self.pos.idx >= len(self._data):
            self.current_char = None
        else:
            self.current_char = self._data[self.pos.idx]

    def whitespace(self):
        while self.current_char is not None and self.current_char in ' \t':
            self.advance()

    def peek(self):
        if (self.pos.idx + 1) < len(self._data):
            return self._data[self.pos.idx + 1]
        return None

    def string(self) -> Token:
        result: str = ''
        delimiter = self.current_char

        self.advance()

        while self.current_char is not None and self.current_char != delimiter:
            result += self.current_char
            self.advance()

        if self.current_char is None or self.current_char != delimiter:
            raise SyntaxError

        self.advance()

        return Token(STRING, result, self.pos)

    def number(self) -> Token:
        result: str = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return Token(NUMBER, int(result), self.pos)

    def dieroll(self) -> Token:
        result: str = ''

        next_char = self.peek()
        if self.current_char is not None and next_char is not None:
            if self.current_char.lower() == 'd' and next_char.isdigit():
                result += self.current_char
                self.advance()

                while (self.current_char is not None
                       and self.current_char.isdigit()):
                    result += self.current_char
                    self.advance()

                return TokenDieRoll(DIEROLL, result.upper())

        raise Exception

    def variable_reference(self) -> Token:
        result: str = ''
        self.advance()
        while (self.current_char is not None and
               (self.current_char.isalpha() or
                self.current_char.isdigit() or
                self.current_char in ['_'])):
            result += self.current_char
            self.advance()

        return Token(REFERENCE, result, self.pos)

    def _id(self) -> Token:
        result: str = ''

        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()

        if result in RESERVED_KEYWORDS:
            return RESERVED_KEYWORDS[result]

        if result in SYSTEM_KEYWORDS:
            return SYSTEM_KEYWORDS[result]

        return Token(ID, result, self.pos)

    def get_next_token(self) -> Token:
        while self.current_char is not None:
            self.whitespace()

            next_char = self.peek()

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+', self.pos)
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-', self.pos)
            elif self.current_char == '*':
                self.advance()
                return Token(MUL, '*', self.pos)
            elif self.current_char == '/' and next_char == '/':
                self.advance()
                self.advance()
                return Token(IDIV, '//', self.pos)
            elif self.current_char == '/':
                self.advance()
                return Token(DIV, '/', self.pos)
            elif self.current_char == '<':
                self.advance()
                return Token(LESSTHAN, '<', self.pos)
            elif self.current_char == '>':
                self.advance()
                return Token(GREATERTHAN, '>', self.pos)
            elif self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(', self.pos)
            elif self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')', self.pos)
            elif self.current_char == '\n':
                while self.current_char == '\n':
                    self.advance()
                return Token(NEWLINE, '\n', self.pos)
            elif self.current_char == ':':
                self.advance()
                return Token(ASSIGN, ':', self.pos)
            elif self.current_char == '"':
                return self.string()
            elif self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')
            elif self.current_char.isdigit():
                return self.number()
            elif (self.current_char.lower() == 'd' and
                  next_char is not None and next_char.isdigit()):
                return self.dieroll()
            elif self.current_char.isalpha():
                return self._id()
            elif (self.current_char == '$'
                  and next_char is not None and next_char.isalpha()):
                return self.variable_reference()
            else:
                pos_start = self.pos.copy()
                raise IllegalCharError(
                    pos_start, self.pos, "'" + self.current_char + "'")

        return Token(EOF, None, self.pos)

    def make_tokens(self) -> List[Token]:
        tokens: List[Token] = []
        while self.current_char is not None:
            tokens.append(self.get_next_token())
        return tokens


if __name__ == '__main__':
    while True:
        text = input('> ')
        res = (Tokenizer(text)).make_tokens()
        print(res)
