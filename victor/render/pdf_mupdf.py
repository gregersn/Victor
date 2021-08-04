from typing import Dict, Any, Iterable, Tuple
from pathlib import Path
import shutil
import fitz


def widget_info(w: fitz.Widget) -> Dict[str, Any]:
    info: Dict[str, Any] = {
        "field": w,
        "next": w.next,
        "border_color": w.border_color,
        "border_style": w.border_style,
        "border_width": w.border_width,
        "border_dashes": w.border_dashes,
        "choice_values": w.choice_values,
        "field_name": w.field_name,
        "field_label": w.field_label,
        "field_value": w.field_value,
        "field_flags": w.field_flags,
        "field_type": w.field_type,
        "field_type_string": w.field_type_string,
        "fill_color": w.fill_color,
        "button_caption": w.button_caption,
        "is_signed": w.is_signed,
        "rect": w.rect,
        "text_color": w.text_color,
        "text_font": w.text_font,
        "text_fontsize": w.text_fontsize,
        "text_maxlen": w.text_maxlen,
        # "text_type": w.text_type,
        "xref": w.xref,
        "text_font": w.text_font
    }

    return info


def fill_pdf_with_mupdf(filename: Path, data: Dict[str, Any], output: Path):
    shutil.copy(filename, output)

    pdf = fitz.Document(str(output))

    for page in pdf:
        widgets: Iterable[fitz.Widget] = page.widgets()
        for field in widgets:
            if field.field_name in data and data[field.field_name] is not None:
                field.field_value = str(data[field.field_name])
                field.update()

    pdf.saveIncr()

    return


def experiment_with_pdf(filename: Path, data: Dict[str, Any], output: Path):
    list_widget_info(str(output))

    # print(data)
    pdf = fitz.Document(str(output))

    fonts = pdf.FormFonts

    print(fonts)

    cat_xref = pdf.pdf_catalog()
    form_fonts = pdf.xref_get_key(cat_xref, "AcroForm/DR/Font")

    font_dict: Dict[str, str] = {}

    for entry in form_fonts[1][3:-2].split('/'):
        name, *values = entry.split(' ')
        font_dict[name] = " ".join(values)

    print(font_dict)
    for page in pdf:
        widgets: Iterable[fitz.Widget] = page.widgets()

        for field in widgets:
            if field.field_type_string in ['CheckBox']:
                # Skip fields that doesn't have a font
                continue
            apn: Tuple[str, str] = pdf.xref_get_key(field.xref, "AP/N")
            apn_id = int(apn[1].split(" ")[0])

            current_font: Tuple[str, str] = pdf.xref_get_key(
                apn_id, "Resources/Font")

            print(current_font)

            # Set the current font to null, to clear it out
            pdf.xref_set_key(apn_id, "Resources/Font", "null")

            # Set the current font based on stuff
            new_font_string: str = f"Resources/Font/{field.text_font}"
            new_font_xref: str = font_dict[field.text_font]

            # print(new_font_string)
            # print(new_font_xref)
            # print(f"{field.field_name}: {current_font[1]}")

            pdf.xref_set_key(
                apn_id, new_font_string, new_font_xref)

    pdf.saveIncr()

    list_widget_info(str(output))


def list_widget_info(filename: str):
    pdf = fitz.Document(filename)

    fonts = pdf.FormFonts

    print(fonts)

    cat_xref = pdf.pdf_catalog()
    form_fonts = pdf.xref_get_key(cat_xref, "AcroForm/DR/Font")

    font_dict = {}

    for entry in form_fonts[1][3:-2].split('/'):
        name, *values = entry.split(' ')
        font_dict[name] = " ".join(values)

    for page in pdf:
        widgets: Iterable[fitz.Widget] = page.widgets()

        for field in widgets:
            if field.field_type_string in ['CheckBox']:
                # Skip fields that doesn't have a font
                continue
            apn: Tuple[str, str] = pdf.xref_get_key(field.xref, "AP/N")
            apn_id = int(apn[1].split(" ")[0])

            print(field.text_font)
            current_font: Tuple[str, str] = pdf.xref_get_key(
                apn_id, "Resources/Font")

            print(current_font)
