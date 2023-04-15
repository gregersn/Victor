"""Victor's guide to creation."""
from typing import Any, Callable, Dict, List, Sequence, Union
import random
from ringneck import run
from trill import trill
import yaml

Tables = Union[List[Any], Dict[Union[int, str], Any]]


def pick_from_random_table(table: Tables) -> Any:
    """Return a random element from a table.

    The table can be a simple list, with equal chance,
    or a dictionary with ranges for each alternative as keys.
    """
    if isinstance(table, list):
        return random.choice(table)

    cum_weights: List[int] = []
    alternatives: List[Any] = []
    for key, value in table.items():
        if isinstance(key, str) and '-' in key:
            weight = int(key.split('-')[-1], 10)
        elif isinstance(key, str):
            weight = int(key, 10)
        else:
            weight = key
        cum_weights.append(weight)
        alternatives.append(value)

    return random.choices(alternatives, cum_weights=cum_weights, k=1)[0]


def ranged_table_lookup(table: Tables, lookup_value: int):
    """Return an element from a table with ranges.

    The table can have gaps."""
    if isinstance(table, list):
        assert isinstance(lookup_value, int)
        return table[lookup_value]

    prev_upper = None
    for key, value in table.items():
        if isinstance(key, str) and '-' in key:
            lower, upper = [int(v, 10) for v in key.split('-')]
            if lookup_value >= lower and lookup_value <= upper:
                return value
            if (lookup_value < lower and prev_upper and lookup_value > prev_upper):
                return value

            prev_upper = upper


def table_lookup(table: Tables, key: Any) -> Any:
    """Straight table lookup."""
    if isinstance(table, dict):
        return table.get(key)
    return table[key]


def roll(definition: str) -> Union[List[int], int, str]:
    """Roll dice expressed with Troll."""
    res = trill(definition)
    return res[0][0]


def load_tables(filename: str):
    """Load table definitions from a file.

    TODO: This should probably not be a callable function from generators,
    but rather a parameter when invoking.
    """
    with open(filename, 'r', encoding="utf8") as file_object:
        data = yaml.safe_load(file_object)
    return data


def swap(left: Any, right: Any):
    """Swap two values."""
    print(left)
    print(right)
    return right, left


def get_interpreter(program: str, global_values: Dict[str, Any]) -> Any:
    """Return an interpreter for Victor."""
    builtins: Dict[str, Callable[..., Any]] = {
        'roll': roll,
        'random_table': pick_from_random_table,
        'table_lookup': table_lookup,
        'load_tables': load_tables,
        'ranged_table': ranged_table_lookup,
        'max': max,
        'swap': swap
    }
    return run(program, builtins=builtins, global_variables=global_values)
