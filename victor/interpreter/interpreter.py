import random
from typing import List, Union, Tuple, Dict, Any
from .ast import (AST, BinOp, Number, DieRoll, UnaryOp,
                  IfNode, Assign, Reference, String)
from .tokens import PLUS, MUL, DIV, IDIV, LESSTHAN, GREATERTHAN, RESERVED
from .nodes import NodeVisitor
from .parser import Parser


class Interpreter(NodeVisitor):
    _parser: Parser
    _tree: Union[AST, List[AST], None]

    def __init__(self, parser: Parser):
        self._parser = parser
        self._tree = None
        self.variables: Dict[str, Any] = {}
        self.output: List[Any] = []

    def interpret(self, **kwargs: Any) -> Tuple[int, List[Any]]:
        if self._tree is None:
            self._tree = self._parser.parse()

        if isinstance(self._tree, list):
            self.output = []
            for v in self._tree:
                self.output.append(self.visit(v, **kwargs))
        else:
            self.output = [self.visit(self._tree, **kwargs), ]

        return 0, self.output

    def visit_BinOp(self, node: BinOp, **kwargs: Any):
        if node.op.type == PLUS:
            return (self.visit(node.left, **kwargs) +
                    self.visit(node.right, **kwargs))

        elif node.op.type == MUL:
            return (self.visit(node.left, **kwargs) *
                    self.visit(node.right, **kwargs))

        elif node.op.type == DIV:
            return (self.visit(node.left, **kwargs) //
                    self.visit(node.right, **kwargs))

        elif node.op.type == IDIV:
            return (self.visit(node.left, **kwargs) //
                    self.visit(node.right, **kwargs))

        elif node.op.type == LESSTHAN:
            return (self.visit(node.left, **kwargs) <
                    self.visit(node.right, **kwargs))

        elif node.op.type == GREATERTHAN:
            return (self.visit(node.left, **kwargs) >
                    self.visit(node.right, **kwargs))

        elif node.op.matches(RESERVED, 'AND'):
            return (self.visit(node.left, **kwargs) and
                    self.visit(node.right, **kwargs))

        elif node.op.matches(RESERVED, 'OR'):
            return (self.visit(node.left, **kwargs) or
                    self.visit(node.right, **kwargs))

        raise NotImplementedError(f"Unknown BinOp {node.op.type}")

    def visit_Number(self, node: Number, **kwargs: Any):
        return node.value

    def visit_DieRoll(self,
                      node: DieRoll,
                      average: bool = False,
                      **kwargs: Any):
        v = node.value.split('D')
        multiplier = int(v[0]) if v[0].isdigit() else 1
        dice_size = int(v[1])

        if average:
            return multiplier * (dice_size + 1) / 2
        else:
            return sum([random.randint(1, dice_size)
                        for _ in range(multiplier)])

    def visit_UnaryOp(self, node: UnaryOp, **kwargs: Any):
        if node.op.value == '-':
            return -self.visit(node.expr, **kwargs)
        return self.visit(node.expr, **kwargs)

    def visit_NoOp(self, node: AST, **kwargs: Any):
        return

    def visit_IfNode(self, node: IfNode, **kwargs: Any):
        for case in node.cases:
            if self.visit(case[0]):
                return self.visit(case[1])

        if node.else_case:
            return self.visit(node.else_case)

        return None

    def visit_Assign(self, node: Assign, **kwargs: Any):
        self.variables[node.left.value] = self.visit(node.right, **kwargs)

        return self.variables[node.left.value]

    def visit_Reference(self, node: Reference, **kwargs: Any):
        return self.variables[node.value]

    def visit_String(self, node: String, **kwargs: Any):
        return node.value
