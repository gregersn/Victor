from typing import Callable, List, Optional, Any, Tuple
from .tokens import (Token, RESERVED, ID, DIEROLL, STRING,
                     NUMBER, REFERENCE, LPAREN, RPAREN, EOF, PLUS, MINUS, MUL,
                     IDIV, DIV, LESSTHAN, GREATERTHAN, ASSIGN, NEWLINE, COMMA)
from .tokenizer import Tokenizer
from .ast import (AST, BinOp, IfNode, Var, NoOp,
                  DieRoll, Number, String, Reference, UnaryOp, Assign, Call)


class Parser:
    _tokens: List[Token]
    _lexer: Tokenizer
    current_token: Optional[Token]

    def __init__(self, lexer: Tokenizer):
        self._lexer = lexer
        self.token_index = -1
        self.current_token = self._lexer.get_next_token()

    def error(self, msg: str = ''):
        raise Exception(
            f"Parsing error at {self.token_index}, {self.current_token}: {msg}")

    def eat(self, _type: str, value: Any = None):
        token = self.current_token
        if token is not None and token.type == _type:
            if value is not None and token.value != value:
                self.error(
                    f"Wrong token value, expected {value}, got {token.value}")

            self.token_index += 1
            self.current_token = self._lexer.get_next_token()

        elif self.current_token is not None:
            self.error(
                f"Wrong token type: {self.current_token.type}, " +
                f"expected {_type}" +
                f":{value}" if value is not None else "" +
                f"\n{self.current_token.pos_start}")
        else:
            self.error("Token underrun")

    def binary_operation(self,
                         func: Callable[[], AST],
                         operators: Tuple[Any, ...]):
        left = func()
        while (self.current_token is not None and
               (self.current_token.type in operators or
                (self.current_token.type, self.current_token.value) in
                operators)):
            token = self.current_token
            self.eat(token.type)

            left = BinOp(left=left, op=token, right=func())
        return left

    def conditional_expr(self):
        """
        conditional_expr : IF expr
                           THEN expr (ELIF expr THEN expr)* (ELSE expr)?
        """

        cases: List[Tuple[AST, AST]] = []
        else_case: Optional[AST] = None
        if self.current_token is None:
            raise EOFError

        self.eat(RESERVED, 'IF')
        condition = self.expr()
        self.eat(RESERVED, 'THEN')
        result = self.expr()

        cases.append((condition, result))

        while (self.current_token is not None and
               self.current_token.matches(RESERVED, 'ELIF')):
            self.eat(RESERVED, 'ELIF')
            condition = self.expr()
            self.eat(RESERVED, 'THEN')
            result = self.expr()

            cases.append((condition, result))

        if (self.current_token is not None
                and self.current_token.matches(RESERVED, 'ELSE')):
            self.eat(RESERVED, 'ELSE')
            else_case = self.expr()

        return IfNode(cases, else_case)

    def compound_statement(self):
        pass

    def variable(self):
        assert self.current_token is not None
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        #  empty:
        return NoOp()

    def function_call(self):
        assert self.current_token is not None
        fun = self.current_token
        params: List[AST] = []
        self.eat(RESERVED)
        self.eat(LPAREN)
        while (self.current_token is not None and
               self.current_token.type != RPAREN):
            params.append(self.expr())
            if self.current_token.type != RPAREN:
                self.eat(COMMA)
        self.eat(RPAREN)

        return Call(fun, params)

    def atom(self) -> AST:
        """
        atom : INT|REF|DIEROLL|ID|STRING
             : LPAREN expr RPAREN
             : conditional_expr
             : function_call
        """
        if self.current_token is not None:
            token = self.current_token
            if token.type == DIEROLL:
                self.eat(DIEROLL)
                return DieRoll(token)
            elif token.type == NUMBER:
                token = token
                self.eat(NUMBER)
                return Number(token)
            elif token.type == STRING:
                token = token
                self.eat(STRING)
                return String(token)
            elif token.type == REFERENCE:
                token = token
                self.eat(REFERENCE)
                return Reference(token)
            elif token.type == LPAREN:
                self.eat(LPAREN)
                token = self.expr()
                self.eat(RPAREN)
                return token
            elif token.type == EOF:
                return NoOp()
            elif token.type == RESERVED and token.value != 'IF':
                return self.function_call()
            else:
                return self.conditional_expr()

        raise EOFError

    def factor(self) -> AST:
        # factor: (PLUS|MINUS) factor |
        #                      NUMBER |
        #                      DIEROLL |
        #                      LPAREN expr RPAREN |
        #                      variable
        # facotr: (PLUS|MINUS) factor | atom
        token = self.current_token

        if token is None:
            raise SyntaxError
        elif token.type == PLUS:
            self.eat(PLUS)
            return UnaryOp(token, self.factor())
        elif token.type == MINUS:
            self.eat(MINUS)
            return UnaryOp(token, self.factor())

        return self.atom()

    def term(self):
        # term:  factor (( MUL | DIV | IDIV ) factor ) *
        return self.binary_operation(self.factor, (MUL, DIV, IDIV))

    def arithmetic_expr(self):
        # arithmetic_expr : term (( PLUS | MINUS ) term ) *
        return self.binary_operation(self.term, (PLUS, MINUS))

    def comparative_expr(self):
        # comparative_expr : NOT comparative_expr
        #                  : arithmetic_expr ((EE | LT | GT | LTE | GTE)
        #                                     arithmetic_expr)*
        return self.binary_operation(self.arithmetic_expr,
                                     (LESSTHAN, GREATERTHAN))

    def assignment_expr(self):
        """
        IDENTIFIER ASSIGN expr
        """
        token = self.variable()
        op = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        assert token is not None
        assert op is not None
        assert right is not None
        return Assign(token, op, right)

    def expr(self) -> AST:
        """
        expr : comparative_expr ((AND | OR) comparative_expr)*
             : IDENTIFIER ASSIGN expr
        """
        if self.current_token is not None and self.current_token.type == ID:
            return self.assignment_expr()

        return self.binary_operation(self.comparative_expr,
                                     ((RESERVED, 'AND'),
                                      (RESERVED, 'OR')))

    def program(self) -> List[AST]:
        """
        program: expr (NEWLINE expr)*
        """
        listing: List[AST] = []

        while (self.current_token is not None and
               self.current_token.type == NEWLINE):
            self.eat(NEWLINE)

        listing.append(self.expr())
        while (self.current_token is not None and
               self.current_token.type == NEWLINE):
            self.eat(NEWLINE)
            listing.append(self.expr())

        return listing

    def parse(self):
        return self.program()
