from typing import List, Dict, Any, Union
import PySimpleGUI as sg
from pathlib import Path

from victor.interpreter import get_interpreter


DEFAULT_PROGRAM = """STR: 3D6
DEX: 3D6
INT: 3D6
HP: ($DEX + $STR) / 10 + 1
"""

MENU_DEF = [['&File', ['&Open', '&Save', 'Save &As...', 'E&xit']]]

current_file: Union[None, Path] = None


def start_gui(*args: List[Any], **kwargs: Dict[str, Any]):
    global current_file
    # sg.theme('DarkAmber')

    layout = [
        [sg.Menu(MENU_DEF)],
        [sg.Text("Input")],
        [sg.Multiline(DEFAULT_PROGRAM,
                      key="input", size=(40, 12))],
        [sg.Text("Output")],
        [sg.Multiline(key="output", size=(40, 12))],
        [sg.Button("Roll"), sg.Button("Average")],
    ]

    window = sg.Window("Victor", layout)
    input_program = ''

    running = True

    while running:
        window_data = window.read()

        if window_data is None:
            continue

        event, values = window_data

        if event == sg.WIN_CLOSED or event == 'Exit':
            # Exit event by breaking out of loop.
            running = False
            break

        if isinstance(values, dict):
            input_program: str = values['input']
            interpreter = get_interpreter(input_program)

            if event == 'Roll':
                interpreter.interpret()

            elif event == 'Average':
                interpreter.interpret(average=True)

            output: sg.Element = window['output']
            output_string = "\n".join(
                [f"{k}: {v}" for k, v in interpreter.variables.items()])
            output.Update(value=output_string)

        if event == 'Open':
            filename: Union[str, None] = sg.popup_get_file(
                "Open definition file.", no_window=True)
            if filename is None:
                continue
            with open(filename, 'r') as f:
                inp: sg.Element = window.Element('input')
                inp.Update(f.read())
            current_file = Path(filename)
            continue

        elif (event == 'Save' and current_file is not None):
            with open(current_file, 'w') as f:
                f.write(input_program)

        elif event == 'Save As...' or (event == 'Save' and current_file is None):
            filename = sg.popup_get_file(
                "Save definition file.", save_as=True, no_window=True)

            if filename:
                current_file = Path(filename)

                with open(current_file, 'w') as f:
                    f.write(input_program)

    window.close()
