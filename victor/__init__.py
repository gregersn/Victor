from typing import Any, Dict, Union
from pathlib import Path

import jinja2

from victor.interpreter import get_interpreter
from victor.render import fill_pdf


def generate(filename: Union[Path, str],
             average: bool = False) -> Dict[str, Any]:
    if isinstance(filename, str):
        filename = Path(filename)

    if not filename.is_file():
        raise FileNotFoundError()

    with open(filename, 'r', encoding="utf8") as f:
        program = f.read()

    state: Dict[str, Any] = {}
    get_interpreter(
        program, state, basedir=filename.absolute().parent, average=average)

    return state


def fill_markdown(filename: Path, data: Any, output: Union[Path, None]):
    template = jinja2.Template(open(filename, 'r', encoding='utf8').read())
    return template.render(**data)


def fill_sheet(
    filename: Union[Path, str],
    character: Any,
    output: Union[Path, str, None],
) -> None:
    if isinstance(filename, str):
        filename = Path(filename)

    if isinstance(output, str):
        output = Path(output)

    assert filename.exists()

    if filename.suffix in ['.pdf']:
        fill_pdf(filename, character.variables, output)

    if filename.suffix in ['.j2']:
        return fill_markdown(filename,
                             character,
                             output)
