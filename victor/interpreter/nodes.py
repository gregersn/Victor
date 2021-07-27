from typing import Any
from .ast import AST


class NodeVisitor:
    def visit(self, node: AST, **kwargs: Any) -> Any:
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, **kwargs)

    def generic_visit(self, node: AST, **kwargs: Any):
        raise Exception(f'No visit_{type(node).__name__} method')
