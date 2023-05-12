from pathlib import Path
from victor.interpreter.generator import get_interpreter


program = """name = ['Wolfgang', 'Amadeus', 'Beethoven']

$.name = random_table(name)
$.STR = roll('sum 3D6')
$.DEX = roll('sum 3D6')
$.INT = roll('sum 3D6')
$.HP = ($.DEX + $.STR) / 10 + 1"""


def test_program():

    result_data = {}

    get_interpreter(
        program, result_data, Path("."), average=True)

    assert result_data
    assert result_data['STR'] == 10.5
    assert result_data['DEX'] == 10.5
    assert result_data['INT'] == 10.5
    assert result_data['HP'] == 3.1
    assert result_data['name'] in ["Wolfgang", "Amadeus", "Beethoven"]
