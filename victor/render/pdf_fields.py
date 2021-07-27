# flake8: noqa
# pyright: reportGeneralTypeIssues=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false

"""
The code in this file is based on code from this comment
https://github.com/pikepdf/pikepdf/issues/58#issuecomment-826374686

"""
from typing import Dict, Any
from typing import cast
from pikepdf import Pdf, Name, String, Array, Page


def get_fields(pdf: Pdf) -> Dict[str, Any]:
    """
    Extract info about the interactive fields present in the AcroForm of the
    pikepdf.PdfObject passed.
    Also, if the PDF has attr: 
        NeedAppearances, ensures that it's value is True.
        param: pdf - instance of<pikepdf.PdfObject>
    returns: None, if the Pdf doesn't have an AcroForm, 
    or a nested dict containing
    the fields names as the keys, with their value being a dict following this 
    specification:
        '/FT' : field type;
        '/V' : current value present in the field;
        '/DV': if the field is one of the text types ('/Tx' or '/Ch'),
        this shows what value is the default one when the field
        has not yet been filled;
        'options': if the field is one of the button types ('/Btn' or '/RBtn'),
        this holds a list that contains the values used to represent when the
        button is `off` or `on`, or `off` and all the values used to represent
        the different options, in case it's a '/RBtn'. This method tries to
        ensure that options[0] will always be the `off` value, but this can't 
        be
        guaranteed to always be true, since some Pdf-Form-Maker softwares might
        not follow all the Pdf 1.7 ISO specs.
    extra_info: some common types of fields:
        '/Tx': Text Field;
        '/Ch': Options List or Combo Box;
        '/Btn': Interactive Button;
        '/RBtn': Radio Button Parent;
        '/Sig': Signature Field (not suported yet, might be in the future)
    """
    if not hasattr(pdf.Root, "AcroForm"):
        return None
    if hasattr(pdf.Root.AcroForm, "NeedAppearances"):
        # If there's NeedAppearances in the Pdf AcroForm,
        # ensure that it's value is True
        pdf.Root.AcroForm.NeedAppearances = True

    fields = {}
    radio_repeats = []
    off_values = (
        "/Off",
        "/No",
        "/0",
        "/Null",
        "/False",
        "/Nill",
    )
    # These are some `off` values that I've seen in some Pdf Forms

    for page in pdf.pages:
        for annot in page.Annots:
            if not hasattr(annot, "FT"):  # This handles kids of radio buttons
                parent_str = str(annot.Parent.T)
                if parent_str in radio_repeats:
                    # check if annot.Parent isn't yet in the repeats list.
                    # if it is, just get the '/Yes' value
                    cur_list = fields[parent_str]["options"]
                    off_value = cur_list[0]
                    options = [
                        item for item in annot.AP.N if item != off_value]
                    cur_list.extend(options)
                    fields[parent_str]["options"] = cur_list
                    continue
                options = [item for item in annot.AP.N]
                # access the kids keys of '/N' to get the
                # '/Off' and '/Yes' values of this first
                # radio button kid
                if options[0] not in off_values:
                    options.reverse()
                info_field = {
                    "/FT": "/RBtn",  # This '/RBtn' notation is not standartized
                    "/V": str(annot.AS),
                    "options": options,
                }
                fields.update({str(annot.Parent.T): info_field})
                radio_repeats.append(parent_str)
            else:
                if annot.FT == "/Btn":
                    if hasattr(annot, "A"):
                        # most likely JS Code utility button.
                        # They're not truly interactive, so skip
                        continue
                    # Else, must be a normal checkbox.
                    # It's way simpler to work with them
                    off_on_values = [item for item in annot.AP.N]
                    if off_on_values[0] not in off_values:
                        # Trying to ensure that index[0] will
                        # always be the '/Off' value
                        off_on_values.reverse()
                    info_field = {
                        "/FT": "/Btn",
                        "/V": str(annot.AS),
                        "options": off_on_values,
                    }
                elif annot.FT == '/Sig':
                    # Placeholder for signatures fields, since I need to
                    # do some research to see how their structure works
                    continue
                else:
                    # Otherwise, must be an text field
                    # ('/Tx' or '/Ch')
                    info_field = {}
                    if hasattr(annot, 'FT'):
                        info_field["/FT"] = str(annot.FT)
                    if hasattr(annot, 'V'):
                        info_field["/V"] = str(annot.V)
                    if hasattr(annot, 'DV'):
                        info_field["/DV"] = str(annot.DV)
                fields.update({str(annot.T): info_field})
    return fields


def update_fields(pdf: Pdf, fields: Dict[str, Any]):
    """
    Update Pdf interactive form fields values
        param: pdf - instance of<pikepdf.PdfObject> to update fields values
        param: fields - dict with fields names and their desired value
    For better performance, it's recommended to send only the fields names
    that need their values updated, as this method does nested iterations.
    The desired values sent are transformed into strings before being updated.
    You can send values that are not originally in fields of the type '/Ch'.
    They'll be added to these interactive fields, and their value switched to
    the desired value.
    warning: this method doesn't try to interpret booleans as `off`/`on` values
    of buttons. Instead, make the values of buttons fields be one of those listed in
    the 'options' list when using get_fields(). Otherwise, the field might not work as expected
    """
    for page in pdf.pages:
        page = Page(page)

        for annot in page.Annots:
            annot = cast()
            for field, item in fields.items():
                value = str(item)
                if not hasattr(annot, "FT"):
                    if str(annot.Parent.T) != field:
                        continue
                    else:
                        foo = Name(value)
                        annot.Parent.AS = foo
                        annot.AS = foo
                        # The Parent holds in it's .AS the `on` value of the kid
                        # that's `on`, but the kid also needs tho have it's .AS
                        # set to the `on` value to show itself the right way
                        continue
                elif field != str(annot.T):
                    continue
                field_type = str(annot.FT)
                if field_type == "/Tx":
                    foo = String(value)
                    annot.V = foo
                    annot.DV = foo
                    # DV's are also updated because this "forces"
                    # most pdfviewers to display them
                elif field_type == "/Btn":
                    if hasattr(annot, "A"):
                        # This skips most JS Code buttons
                        continue
                    foo = String(value)
                    annot.AS = Name(value)
                    annot.V = foo
                    annot.DV = foo
                    # Normal checkboxes (usually) hold their values
                    # both in the AS and V
                elif field_type == "/Ch":
                    opt_list = [str(item) for item in annot.Opt]
                    if value not in opt_list:
                        # Add the value to the original '/Opt' -- why
                        # limit yourself to only the values that the pdf form
                        # creator wants you to use?
                        opt_list.append(value)
                        opt_list.sort()
                        annot.Opt = Array(opt_list)
                    foo = String(value)
                    annot.V = foo
                    annot.DV = foo
                elif field_type == "/Sig":
                    # Placeholder for signature fields. Needs more research
                    continue
