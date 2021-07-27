from typing import Union
from pathlib import Path

from victor.character import Character
from .pdf_fields import update_fields

from pikepdf import Pdf


def fill_pdf(filename: Union[Path, str],
             character: Character,
             output: Union[Path, str, None]) -> None:
    if isinstance(filename, str):
        filename = Path(filename)

    assert filename.is_file()

    if output is None:
        output = Path("./output.pdf")

    with Pdf.open(filename) as sheet:
        update_fields(sheet, character.variables)
        sheet.save(output)
