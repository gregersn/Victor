from .tokens import (Token, TokenDieRoll)
from .tokens import (STRING, DIEROLL, NUMBER,
                     REFERENCE, ID, PLUS, MINUS, MUL, IDIV, DIV,
                     LESSTHAN, GREATERTHAN, LPAREN, RPAREN,
                     ASSIGN, NEWLINE, EOF)
from .keywords import RESERVED_KEYWORDS
from typing import List, Optional
from .position import Position


class Error(BaseException):
    def __init__(self,
                 pos_start: Position,
                 pos_end: Position,
                 name: str,
                 details: str):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.name = name
        self.details = details

    def __str__(self):
        return (f'{self.name}: {self.details}' +
                f' at {self.pos_start.ln}, {self.pos_start.col}')


class IllegalCharError(Error):
    def __init__(self, pos_start: Position, pos_end: Position, details: str):
        super().__init__(pos_start, pos_end, "Illegal character", details)


class Tokenizer:
    _data: str
    pos: Position
    current_char: Optional[str]
    filename: str

    def __init__(self, data: str = ""):
        self._data = data
        self.filename = ""
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

        return Token(NUMBER, int(result), self.pos)

    def variable_reference(self) -> Token:
        result: str = ''
        self.advance()
        while (self.current_char is not None and
               (self.current_char.isalpha() or self.current_char.isdigit())):
            result += self.current_char
            self.advance()

        return Token(REFERENCE, result, self.pos)

    def _id(self) -> Token:
        result: str = ''

        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()

        return RESERVED_KEYWORDS.get(result, Token(ID, result, self.pos))

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
            elif (self.current_char.lower() == 'd' and
                  next_char is not None and next_char.isdigit()):
                return self.number()
            elif self.current_char.isalpha():
                return self._id()
            elif self.current_char.isdigit():
                return self.number()
            elif self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(', self.pos)
            elif self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')', self.pos)
            elif (self.current_char == '$'
                  and next_char is not None and next_char.isalpha()):
                return self.variable_reference()
            elif self.current_char == ':':
                self.advance()
                return Token(ASSIGN, ':', self.pos)
            elif self.current_char == '\n':
                self.advance()
                return Token(NEWLINE, '\n', self.pos)
            elif self.current_char == '"':
                return self.string()
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
