from typing import Any, Generic, List, Optional, TypeVar

import random

T = TypeVar('T')


class RandomTable(Generic[T]):
    alternatives: List[T]
    range: List[int]

    def __init__(self, alternatives: List[T], _range: Optional[List[int]] = None):
        self.alternatives = alternatives
        self.range = _range or [x + 1 for x in range(len(alternatives))]
        assert len(self.alternatives) == len(self.range)

    def get(self, value: int):
        f = next(x[0] for x in enumerate(self.range) if x[1] >= value)
        return self.alternatives[f]

    def __len__(self):
        return self.range[-1]

    def __call__(self) -> Any:
        return self.get(random.randint(1, len(self)))


def main():

    table = RandomTable(['human', 'halfling', 'dwarf', 'elf',
                        'mallard', 'wolfkin'], [4, 7, 9, 10, 11, 12])

    assert len(table) == 12, len(table)

    assert table.get(1) == 'human'
    assert table.get(2) == 'human'
    assert table.get(3) == 'human'
    assert table.get(4) == 'human'
    assert table.get(5) == 'halfling'
    assert table.get(6) == 'halfling'
    assert table.get(7) == 'halfling'
    assert table.get(8) == 'dwarf'
    assert table.get(9) == 'dwarf'
    assert table.get(10) == 'elf'
    assert table.get(11) == 'mallard'
    assert table.get(12) == 'wolfkin'


if __name__ == '__main__':
    main()
