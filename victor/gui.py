"""Victor GUI."""
import os
from typing import List, Dict, Any, Union
from pathlib import Path
import tkinter as tk
import customtkinter as ctk
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

    app = ctk.CTk()
    app.geometry("1000x600")
    app.title("Victor")

    label_input = ctk.CTkLabel(app, text="Input")
    text_input = ctk.CTkTextbox(app)
    label_output = ctk.CTkLabel(app, text="Output")
    text_output = ctk.CTkTextbox(app)

    def open_file():
        global current_file
        filename = ctk.filedialog.askopenfilename()

        if filename:
            current_file = Path(filename)

            with open(current_file, "r", encoding="utf8") as file_handle:
                text_input.delete("0.0", "end")
                text_input.insert("0.0", file_handle.read())

    def save_file(filename: str | Path | None, select: bool = False):
        global current_file
        if not filename or select:
            filename = ctk.filedialog.asksaveasfilename()

        if filename:
            current_file = Path(filename)
            with open(current_file, "w", encoding="utf8") as file_handle:
                file_handle.write(text_input.get("0.0", "end"))

    menu_bar = tk.Menu(app)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open", underline=0, command=open_file)
    file_menu.add_command(
        label="Save", underline=0, command=lambda: save_file(current_file)
    )
    file_menu.add_command(
        label="Save As...",
        underline=5,
        command=lambda: save_file(current_file, select=True),
    )
    file_menu.add_command(label="Exit", underline=1, command=lambda: app.quit())
    menu_bar.add_cascade(label="File", menu=file_menu, underline=0)

    app.config(menu=menu_bar)

    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)

    text_input.insert("0.0", DEFAULT_PROGRAM)
    text_output.configure(state="disabled")

    def roll_callback(average: bool = False):
        input_program = text_input.get("0.0", "end")

        result_data = {}

        get_interpreter(
            input_program,
            result_data,
            current_file.parent if current_file is not None else Path(os.getcwd()),
            average=average,
        )

        output_string = result2string(result_data)

        text_output.configure(state="normal")
        text_output.delete("0.0", "end")
        text_output.insert("0.0", output_string)
        text_output.configure(state="disabled")

    button_roll = ctk.CTkButton(app, text="Roll", command=lambda: roll_callback())
    button_average = ctk.CTkButton(
        app, text="Average", command=lambda: roll_callback(True)
    )

    label_input.grid(row=0, column=0)
    label_output.grid(row=0, column=1)
    text_input.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    text_output.grid(row=1, column=1, padx=10, pady=10, stick="nsew")
    button_roll.grid(row=3, column=0, padx=10, pady=10)
    button_average.grid(row=3, column=1, padx=10, pady=10)

    app.mainloop()
