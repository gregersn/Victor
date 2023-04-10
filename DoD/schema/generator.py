import random
from typing import Any, List, Optional, Type, Dict, Union
from pydantic import BaseModel
import yaml
from pathlib import Path
from trill import trill


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


def ranged_table_lookup(table: Tables, lookup_value: Union[int, str]):
    if isinstance(table, list):
        assert isinstance(lookup_value, int)
        return table[lookup_value]

    prev_upper = None
    for key, value in table.items():
        if isinstance(key, str) and '-' in key:
            lower, upper = [int(v, 10) for v in key.split('-')]
            if lookup_value >= lower and lookup_value <= upper:
                return value
            if lookup_value < lower and prev_upper and lookup_value > prev_upper:
                return value

            prev_upper = upper


class GeneratorField(BaseModel):
    type: str = "generator_field"
    group: Optional[Union[List[str], 'GeneratorField']]

    class Config:
        extra = 'allow'


class RandomTableField(GeneratorField):
    type = "random_table"
    table: str


class RangedTableField(GeneratorField):
    type = "ranged_table"
    table: str


class PickFromTable(GeneratorField):
    type = "pick_from_table"
    table: str
    count: int


class ReferenceField(GeneratorField):
    type = "reference"
    value: str


class SetField(GeneratorField):
    type = "set"
    sub: str
    value: GeneratorField


GeneratorFields = Union[GeneratorField, RandomTableField]


def resolve(path: List[str], source: Dict[str, Any]):
    output = source
    while path:
        key = path.pop(0)
        output = output[key]

    return output


class BaseGenerator(BaseModel):
    tables: Dict[str, Any]
    fields: Dict[str, Union[GeneratorFields, str]]

    @classmethod
    def load(cls, filename: Path):
        with open(filename, 'r', encoding="utf8") as f:
            return cls(**yaml.safe_load(f))

    def generate(self, output_model: Union[BaseModel, Type[BaseModel]]):
        if isinstance(output_model, BaseModel):
            print("Using old")
            output = output_model
        else:
            print("Creating new")
            output = output_model.construct()

        for key, item in self.fields.items():
            print(f"** Working on {key}")
            if getattr(output, key, None):
                print(f"Skipping {key}")
                continue
            if isinstance(item, str):
                setattr(output, key, self.expand(item, output))
                continue
            if item.group:
                if isinstance(item.group, GeneratorField):
                    group_list = self.evaluate(item.group, output, key)
                else:
                    group_list = item.group
                for group_key in group_list:
                    print(f"Setting: {group_key}")
                    setattr(output, group_key, self.evaluate(
                        item, output, group_key))
            else:
                setattr(output, key, self.evaluate(item, output, key))
        return output

    def resolve_addr(self, addr: str, output: BaseModel):
        parts = addr.split('.')
        for idx, part in enumerate(parts):
            if part[0] == '$':
                parts[idx] = getattr(output, part[1:])
        return parts

    def expand(self, value: str, output: BaseModel):
        if value[0] == '$':
            return getattr(output, value[1:])
        return value

    def evaluate_table_value(self, field, output: BaseModel):
        field = RandomTableField.parse_obj(field)
        table = resolve(self.resolve_addr(field.table, output), self.tables)
        return table

    def evaluate_ranged_table(self, field, output: BaseModel):
        field = RangedTableField.parse_obj(field)
        table = resolve(self.resolve_addr(
            field.table, output)[:-1], self.tables)

        lookup_value = getattr(output, field.table.split('.')[-1][1:])

        return ranged_table_lookup(table, lookup_value)

    def evaluate_random_table(self, field, output: BaseModel):
        table = self.evaluate_table_value(field, output)
        return pick_from_random_table(table)

    def evaluate_pick_from_table(self, field, output: BaseModel):
        field = PickFromTable.parse_obj(field)
        table = self.evaluate_table_value(field, output)
        return random.sample(table, k=field.count)

    def evaluate_add(self, field, output: BaseModel, target: str):
        return self.evaluate(GeneratorField(**field.left), output, target) + self.evaluate(GeneratorField(**field.right), output, target)

    def evaluate_multiply(self, field, output: BaseModel, target: str):
        return self.evaluate(GeneratorField(**field.left), output, target) * self.evaluate(GeneratorField(**field.right), output, target)

    def evaluate_reference(self, field, output: BaseModel, target: Optional[str]):
        field = ReferenceField.parse_obj(field)
        path = field.value.split('.')
        result = output
        while path:
            part = path.pop(0)
            if part == "$$":
                result = getattr(result, target)
                continue

            result = getattr(result, part)
        return result

    def evaluate_set(self, field, output: BaseModel, target: str):
        field = SetField.parse_obj(field)
        value_holder = getattr(output, target)
        setattr(value_holder, field.sub, self.evaluate(
            field.value, output, target))
        return value_holder

    def evaluate(self, field: GeneratorField, output: BaseModel, target: Optional[str] = None):
        if field.type == 'table_value':
            return self.evaluate_table_value(field, output)
        if field.type == 'random_table':
            return self.evaluate_random_table(field, output)
        if field.type == 'ranged_table':
            return self.evaluate_ranged_table(field, output)
        if field.type == 'roll':
            return trill(field.expression)[0][-1]
        if field.type == 'add':
            return self.evaluate_add(field, output, target)
        if field.type == 'multiply':
            return self.evaluate_multiply(field, output, target)
        if field.type == 'reference':
            return self.evaluate_reference(field, output, target)
        if field.type == 'constant':
            return field.value
        if field.type == 'pick_from_table':
            return self.evaluate_pick_from_table(field, output)
        if field.type == 'set':
            return self.evaluate_set(field, output, target)
        raise NotImplementedError(f"No evaluator for field type: {field.type}")
