from typing import List, Tuple, Optional, Any
from .tokens import Token


class AST:
    def __init__(self, *args: List[Any], **kwargs: Any) -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class DieRoll(AST):
    token: Token
    value: str

    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"<DiceRoll {self.value}>"


class Number(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self) -> str:
        return f"<Number {self.value}>"


class String(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


class Reference(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self) -> str:
        return f"<Reference {self.value}>"


class UnaryOp(AST):
    def __init__(self, op: Token, expr: AST):
        self.token = self.op = op
        self.expr = expr

    def __repr__(self) -> str:
        return f"<UnaryOp {self.op.value} {self.expr}>"


class BinOp(AST):
    left: AST
    op: Token
    right: AST
    token: Token

    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"<BinOp {self.left} {self.op.value} {self.right}>"


class NoOp(AST):
    def __init__(self, *args: Any, **kwargs: Any):
        pass


class IfNode(AST):
    def __init__(self, cases: List[Tuple[AST, AST]],
                 else_case: Optional[AST] = None):
        self.cases = cases
        self.else_case = else_case


class Var(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"<Var {self.value}>"


class Assign(AST):
    def __init__(self, left: Var, op: Token, right: AST):
        self.left = left
        self.token = self.op = op
        self.right = right
