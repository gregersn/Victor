from pathlib import Path
from typing import List

from generator import GeneratorField

import yaml


class Tables:
    data: List[GeneratorField] = []

    def __init__(self, filename: Path):
        with open(filename, "r", encoding="utf8") as f:
            self.data = yaml.safe_load(f)

    def get(self, table_name: str):
        return self.data[table_name]
        for table in self.data:
            if table['title'] == table_name:
                return table


dod_tables = Tables('dod_tables2.yml')


if __name__ == '__main__':
    # print(NPC.generate())
    # print(NPC.schema_json(indent=2))
    # Character.generate().sheet()
    """
    DodGenerator = Generator(entries={
        'kin': dod_tables.get('Kin'),
        'abilities': dod_tables.get('Abilities'),
        'profession': dod_tables.get('Profession'),
        'name': dod_tables.get('Name')},
    )

    character = DodGenerator.generate(Character)
    print(character)
    """

    print(Character.schema_json(indent=2))
