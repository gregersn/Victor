import random
from typing import Any, Dict, List, Literal, Optional, Type, Union
from pydantic import BaseModel

from schema.sheet import BaseSheet

Tables = Union[List[Any], Dict[Union[int, str], Any]]


def pick_from_random_table(table: Tables):
    if isinstance(table, list):
        return random.choice(table)

    cum_weights = []
    alternatives = []
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


class GeneratorField(BaseModel):
    # type: str
    dependencies: List[str] = []
    title: str
    description: Optional[str]
    entries: Optional[Tables]
    candidates: Optional[Tables]
    roll: Optional[str]

    def evaluate(self, output: BaseSheet):
        if self.candidates:
            result = pick_from_random_table(self.candidates)
        elif self.roll:
            return 4
        elif self.entries:
            result = self.entries
        for dep in self.dependencies:
            if dep[0] == '$':
                key = getattr(output, dep[1:])
            else:
                key = dep
            result = result[key]

        if 'candidates' in result:
            result = pick_from_random_table(result['candidates'])

        return result

    def evaulate_random(self, output: BaseSheet):
        cum_weights = []
        alternatives = []
        for key, value in self.entries.items():
            if isinstance(key, str) and '-' in key:
                weight = int(key.split('-')[-1], 10)
            elif isinstance(key, str):
                weight = int(key, 10)
            else:
                weight = key
            cum_weights.append(weight)
            alternatives.append(value)

        return random.choices(alternatives, cum_weights=cum_weights, k=1)[0]


FieldTypes = Union[GeneratorField, None]


class Generator(BaseModel):
    entries: Dict[str, FieldTypes] = {}

    def generate(self, sheet: Type[BaseSheet]):
        output = sheet.construct()

        for name, generator in self.entries.items():
            if hasattr(output, name):
                print(name, type(getattr(output, name)))
            setattr(output, name, generator.evaluate(output))

        return output


if __name__ == '__main__':
    print(Generator.schema_json(indent=2))
