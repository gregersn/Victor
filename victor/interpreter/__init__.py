from typing import Any, Optional, Dict
from .tokenizer import Tokenizer
from .parser import Parser
from .interpreter import Interpreter


def interpret(program: str, **kwargs: Any):
    interpreter = get_interpreter(program)
    return interpreter.interpret(**kwargs)


def get_interpreter(program: str = "", variables: Optional[Dict[str, Any]] = None):
    tokenizer = Tokenizer(program)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser)
    if variables is not None:
        interpreter.variables = variables
    return interpreter
