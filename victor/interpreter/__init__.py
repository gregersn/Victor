from typing import Any, Dict, Sequence
import random
from ringneck import run
from trill import trill

def roll(input: str):
    res = trill(input)
    return res[0][0]

def random_choice(input: Sequence[Any]):
    return random.choice(input)

def get_interpreter(program: str, global_values: Dict[str, Any]):
    builtins = {
        'roll': roll,
        'random_choice': random_choice
    }
    return run(program, builtins=builtins, global_variables=global_values)
