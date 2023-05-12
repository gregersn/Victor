"""Victor GUI."""
import os
from typing import List, Dict, Any, Tuple, Union, cast
from pathlib import Path
import PySimpleGUI as sg

from victor.interpreter import get_interpreter
from victor.render.utils import result2string

DEFAULT_PROGRAM = """name = ['Wolfgang', 'Amadeus', 'Beethoven']

$.STR = roll('sum 3D6')
$.DEX = roll('sum 3D6')
$.INT = roll('sum 3D6')
$.HP = round_up(($.DEX + $.STR) / 10 + 1)
$.NAME = random_table(name)
"""

current_file: Union[None, Path] = None


def start_gui(*args: List[Any], **kwargs: Dict[str, Any]):
    """Run Victor GUI."""
    global current_file
    # sg.theme('DarkAmber')

    # Create the menu definition.
    MENU_DEFINITION = [['&File', ['&Open', '&Save', 'Save &As...', 'E&xit']]]

    # Specify the layout of the Window
    layout = [
        [sg.Menu(MENU_DEFINITION)],
        [sg.Text("Input")],
        [sg.Multiline(DEFAULT_PROGRAM, key="-INPUT-",
                      size=(40, 12), expand_x=True, expand_y=True)],
        [sg.Text("Output")],
        [sg.Multiline(key="-OUTPUT-", size=(40, 12),
                      expand_x=True, expand_y=True)],
        [sg.Button("Roll"), sg.Button("Average")],
    ]

    window = sg.Window("Victor", layout, resizable=True)
    input_program = DEFAULT_PROGRAM

    running = True

    while running:
        window_data = cast(None | Tuple[str, Dict[Any, Any]], window.read())

        if not isinstance(window_data, tuple):
            continue

        event, values = window_data

        if event in [sg.WIN_CLOSED, 'Exit']:
            # Exit event by breaking out of loop.
            running = False

        # Menu command events
        elif event == 'Open':
            filename = cast(
                None | str,
                sg.popup_get_file("Open Victor file.",
                                  file_types=(
                                      ('Victor files', '*.vic'),
                                      ('All files', '*.* *'),
                                  ),
                                  no_window=True,
                                  history=True))
            if filename:
                current_file = Path(filename)

                with open(current_file, 'r', encoding="utf8") as file_handle:
                    inp: sg.Multiline = cast(
                        sg.Multiline, window.Element('-INPUT-'))
                    inp.Update(file_handle.read())

            continue

        elif (event == 'Save' and current_file is not None):
            with open(current_file, 'w', encoding="utf8") as file_handle:
                file_handle.write(input_program)

        elif event == 'Save As...' or (event == 'Save' and current_file is None):
            filename = cast(None | str, sg.popup_get_file(
                "Save definition file.", save_as=True, no_window=True))
            if filename:
                current_file = Path(filename)

                with open(current_file, 'w', encoding="utf8") as file_handle:
                    file_handle.write(input_program)

        elif event in ['Roll', 'Average']:
            input_program: str = values['-INPUT-']
            assert isinstance(input_program, str)
            result_data = {}

            average = event == 'Average'

            get_interpreter(input_program,
                            result_data,
                            current_file.parent if current_file is not None else Path(
                                os.getcwd()),
                            average=average)

            output = cast(sg.Multiline, window['-OUTPUT-'])
            output_string = result2string(result_data)
            output.Update(value=output_string)
        else:
            raise NotImplementedError(event)

    window.close()
