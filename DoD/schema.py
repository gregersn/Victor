from typing import Any, List, Literal
from pydantic import BaseModel, Field
from trill import trill

from table import RandomTable
from tables import name


Attribute = Literal['STR', 'CON', 'AGL', 'INT', 'WIL', 'CHA']


class Generator():
    ...


class Kin(Generator):
    name: str
    ability: List[str]


Human = Kin(name=name['human'], ability=['Adaptive'])
Halfling = Kin(name=name['halfling'], ability=['Hard to catch'])


class CoreSkill(Generator):
    name: str
    attribute: Attribute


class Profession(Generator):
    key_attribute: Attribute
    skills: List[CoreSkill]
    heroic_ability: str
    gear: Any
    nickname: Any


class Character(Generator):
    kin: Kin = RandomTable([Human, Halfling])
    profession: Profession


def attribute_roll():
    return trill("sum largest 3 4d6")[0][0]


if __name__ == '__main__':
    character = Character()
    print(character)
