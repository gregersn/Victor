from typing import List, Dict, Any
import PySimpleGUI as sg

from victor.interpreter import get_interpreter


DEFAULT_PROGRAM = """STR: 3D6
DEX: 3D6
INT: 3D6
HP: ($DEX + $STR) / 10 + 1
"""


def start_gui(*args: List[Any], **kwargs: Dict[str, Any]):
    # sg.theme('DarkAmber')

    layout = [
        [sg.Text("Input")],
        [sg.Multiline(DEFAULT_PROGRAM,
                      key="input", size=(40, 12))],
        [sg.Text("Output")],
        [sg.Multiline(key="output", size=(40, 12))],
        [sg.Button("Roll"), sg.Button("Average")],
    ]

    window = sg.Window("Victor", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        input_program = values['input']

        interpreter = get_interpreter(input_program)

        if event == 'Roll':
            interpreter.interpret()

        if event == 'Average':
            interpreter.interpret(average=True)

        output = window.Element('output')
        output_string = "\n".join(
            [f"{k}: {v}" for k, v in interpreter.variables.items()])
        output.Update(value=output_string)
    window.close()
