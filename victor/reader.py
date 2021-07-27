from typing import Union, Dict, List
from pathlib import Path


def load_rules(path: Union[Path, str]):
    if isinstance(path, str):
        path = Path(path)
    assert path.exists()

    with open(path, 'r') as f:
        data = f.read()

    t = data.split('---\n')

    return t


def dict2program(d: Dict[str, str]):
    t: List[str] = []
    for k, v in d.items():
        t.append(f'{k}: {v}')

    return "\n".join(t)
