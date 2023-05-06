from re import A
from typing import Any, Dict, Union
from pathlib import Path
from victor.interpreter import get_interpreter

from victor.reader import load_rules

from victor.render import fill_pdf
from victor.character import Character


def generate(filename: Union[Path, str], average: bool = False) -> Dict[str, Any]:
    if isinstance(filename, str):
        filename = Path(filename)

    if not filename.is_file():
        raise FileNotFoundError()

    with open(filename, 'r', encoding="utf8") as f:
        program = f.read()

    state: Dict[str, Any] = {}
    interpreter = get_interpreter(
        program, state, basedir=filename.absolute().parent)

    return state


def fill_sheet(filename: Union[Path, str],
               character: Character,
               output: Union[Path, str, None]) -> None:
    fill_pdf(filename, character.variables, output)
