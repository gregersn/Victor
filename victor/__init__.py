from typing import Union
from pathlib import Path

from victor.reader import load_rules
from victor.interpreter import Tokenizer, Parser, Interpreter

from victor.render import fill_pdf
from victor.character import Character


def generate(filename: Union[Path, str], average: bool = False) -> Character:
    if isinstance(filename, str):
        filename = Path(filename)

    if not filename.is_file():
        raise FileNotFoundError()

    _, metadata, content = load_rules(filename)

    tokenizer = Tokenizer(metadata)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser)
    _ = interpreter.interpret(average=average)

    char = Character()
    char.variables = interpreter.variables
    char.content = content
    return char


def fill_sheet(filename: Union[Path, str],
               character: Character,
               output: Union[Path, str, None]) -> None:
    fill_pdf(filename, character.variables, output)
