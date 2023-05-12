from typing import Any, Dict, Union
from pathlib import Path
from victor.interpreter import get_interpreter
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
    get_interpreter(program, state, basedir=filename.absolute().parent, average=average)

    return state


def fill_sheet(
    filename: Union[Path, str],
    character: Character,
    output: Union[Path, str, None],
) -> None:
    fill_pdf(filename, character.variables, output)
