"""Victor's guide to creation."""
import sys
import math
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union
import random

import yaml

from ringneck import run
from trill import trill

Tables = Union[List[Any], Dict[Union[int, str], Any]]

seed = random.randrange(sys.maxsize)
# seed = 6142246949006077372
random.seed(seed)


def pick_from_random_table(table: Tables, count: int = 1) -> Any:
    """Return a random element from a table.

    The table can be a simple list, with equal chance,
    or a dictionary with ranges for each alternative as keys.
    """
    result = None

    if isinstance(table, set):
        table = list(table)
    if isinstance(table, list):
        result = random.sample(table, k=min(count, len(table)))

    if isinstance(table, dict):
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

        result = random.choices(alternatives, cum_weights=cum_weights, k=count)

    if count == 1 and result:
        return result[0]
    return result


def nested_random_table(table: Tables) -> Any:
    res = pick_from_random_table(table)
    while isinstance(res, list):
        res = pick_from_random_table(res)

    return res


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


def roll(definition: str, average: bool = False) -> Union[List[int], int, str]:
    """Roll dice expressed with Troll."""
    res = trill(definition, random.randrange(sys.maxsize), average=average)
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
    return right, left


def swap_largest(candidates: Any, target: str):
    """Swap the largest value in candidates with target."""
    largest_value = -math.inf
    largest_key = None
    for candidate in candidates:
        value = globals.get(candidate, -math.inf)
        if value > largest_value:
            largest_value = value
            largest_key = candidate

    target_value = globals[target]
    globals[target] = largest_value
    globals[largest_key] = target_value


def apply_modifiers(modifiers: Dict[str, int]):
    """Add values in modifiers to global variables."""
    for key, value in modifiers.items():
        if key not in globals:
            globals[key] = value
        else:
            globals[key] += value


def rand(a: int, b: Optional[int] = None, average: bool = False):
    """Return a random integer."""
    if b is None:
        b = a
        a = 0

    if average:
        return (b - a) / 2

    return random.randrange(a, b)


def distribute(points: int, bin_count: int, average: bool = False):
    """Randomly distribute points among bins."""

    if average:
        return (points / bin_count, ) * bin_count

    bins = [
        0,
    ] * bin_count

    for _ in range(points):
        bins[random.randint(0, bin_count - 1)] += 1

    return tuple(bins)


def evaluate(expression: str):
    """Evaluate expression."""
    result = run(expression, builtins={**globals, 'max': max})

    return result[-1] if result is not None else None


def assign(values: List[Any], variables: List[str]):
    """Assign values to variable names."""
    for var, value in zip(variables, values):
        globals[var] = value


def get_interpreter(
    program: str,
    global_values: Dict[str, Any],
    basedir: Path,
    average: bool = False,
) -> Any:
    """Return an interpreter for Victor."""
    builtins: Dict[str, Callable[..., Any]] = {
        'roll': lambda x: roll(x, average=average),
        'min': min,
        'max': max,
        'swap': swap,
        'swap_largest': swap_largest,
        'apply_modifiers': apply_modifiers,
        'print': print,
        'round_up': lambda x: int(math.ceil(x)),
        'round_down': lambda x: int(math.floor(x)),
        'random': lambda x, y = None: rand(x, y, average=average),
        'distribute': lambda x, y: distribute(x, y, average=average),
        'evaluate': evaluate,
        'len': len,
        'assign': assign,
        'load_tables': lambda x: load_tables(basedir / x),
        'random_table': pick_from_random_table,
        'nested_random_table': nested_random_table,
        'ranged_table': ranged_table_lookup,
        'table_lookup': table_lookup,
    }
    return run(program, builtins=builtins, global_variables=global_values)
