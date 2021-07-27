from typing import Any
from .tokenizer import Tokenizer
from .parser import Parser
from .interpreter import Interpreter


def interpret(program: str, **kwargs: Any):
    tokenizer = Tokenizer(program)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser)
    return interpreter.interpret(**kwargs)
