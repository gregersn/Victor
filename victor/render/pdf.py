from typing import Union, Dict, Any, TypedDict
from pathlib import Path
import yaml

from .field_mapping import remap_reverse
from .pdf_mupdf import fill_pdf_with_mupdf


class AdvancedInfo(TypedDict):
    pdf: Path
    fields: Dict[str, Any]


def advanced_fill(pdf_data: Path,
                  data: Path) -> AdvancedInfo:
    new_values = remap_reverse(values=data, schema=pdf_data)
    return new_values


def fill_pdf(template: Union[Path, str],
             data: Union[Path, str],
             output: Union[Path, str, None]) -> None:
    if isinstance(template, str):
        template = Path(template)

    if isinstance(data, str):
        data = Path(data)

    assert template.is_file()
    assert data.is_file()

    if output is None:
        output = Path("./output.pdf")
    elif isinstance(output, str):
        output = Path(output)

    pdf_data = None
    if template.suffix == '.yaml':
        with open(template, 'r') as f:
            pdf_data = yaml.safe_load(f)

    character_data = None
    if data.suffix == '.yaml':
        with open(data, 'r') as f:
            character_data = yaml.safe_load(f)

    assert pdf_data is not None
    assert character_data is not None

    fill_info = advanced_fill(template, data)

    template_file = fill_info['pdf']
    values = fill_info['fields']

    fill_pdf_with_mupdf(template_file, values, output)
