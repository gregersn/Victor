from typing import List
from pydantic import BaseModel, Field
from pydantic.fields import ModelField
from table import RandomTable


class GeneratorField(ModelField):
    ...


class Generator(BaseModel):
    @classmethod
    def generate(cls):
        schema = cls.schema()
        output = cls.construct()
        for property, field in schema['properties'].items():
            value = "default"
            if 'generator' in field:
                value = field['generator']()

            setattr(output, property, value)

        return output


class Attributes(Generator):
    str: int
    con: int
    agl: int
    int_: int
    wil: int
    cha: int


class Conditions(Generator):
    exhausted: bool
    sickly: bool
    dazed: bool
    angry: bool
    scared: bool
    disheartened: bool


class Character(Generator):
    kin: str = Field(
        name="KIN",  generator=RandomTable(['Human', 'Halfling', 'Dwarf', 'Elf', 'Mallard', 'Wolfkin'], [4, 7, 9, 10, 11, 12]))
    age: str
    profession: str
    weakness: str
    name: str
    appearance: str
    attributes: Attributes
    conditions: Conditions
    damage_bonus_str: str
    damage_bonus_agl: str
    movemenet: int
    abilities_and_spells: List[str]


def main():
    character = Character.generate()
    print(character)


if __name__ == "__main__":
    main()
