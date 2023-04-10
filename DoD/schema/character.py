from enum import Enum
from typing import Dict, List, Literal, Tuple

from pydantic import Field
from common import Kin, Profession
from generator import BaseGenerator
from sheet import BaseSheet

from trill import trill


class Age(str, Enum):
    young = 'Young'
    droid = 'Adult'
    old = 'Old'


class DamageBonus(str, Enum):
    none = '--'
    d4 = '+D4'
    d6 = '+D6'


def attribute():
    return trill('sum largest 3 4d6')[0][0]


class Skill(BaseSheet):
    value: int = 0
    checked: bool = False


class SkillAGL(Skill):
    attribute = Field('AGL', const=True, frozen=True)


class SkillINT(Skill):
    attribute = Field('INT', const=True, frozen=True)


class SkillCHA(Skill):
    attribute = Field('CHA', const=True, frozen=True)


class SkillSTR(Skill):
    attribute = Field('STR', const=True, frozen=True)


class Weapon(BaseSheet):
    weapon_shield: str
    grip: str
    range: str
    damage: str
    durability: str
    features: str


class Character(BaseSheet):
    name: str = ""
    kin: Kin
    age: Age
    profession: Profession
    weakness: str
    appearance: str
    STR: int = Field(title="Strength")
    exhausted: bool = False
    CON: int = Field(title="Constitution")
    sickly: bool = False
    AGL: int = Field(title="Agility")
    dazed: bool = False
    INT: int = Field(title="Intelligence")
    angry: bool = False
    WIL: int = Field(title="Willpower")
    scared: bool = False
    CHA: int = Field(title="Charisma")
    disheartened: bool = False

    damage_bonus_strength: DamageBonus
    damage_bonus_agility: DamageBonus

    movement: int

    abilities: List[str] = Field([], title="Abilities and spells")

    gold: int = 0
    silver: int = 0
    copper: int = 0

    acrobatics: SkillAGL = SkillAGL()
    awareness: SkillINT = SkillINT()
    bartering: SkillCHA = SkillCHA()
    beast_lore: SkillINT = SkillINT()
    bluffing: SkillCHA = SkillCHA()
    bushcraft: SkillINT = SkillINT()
    crafting: SkillSTR = SkillSTR()
    evade: SkillAGL = SkillAGL()
    healing: SkillINT = SkillINT()
    hunting_and_fishing: SkillAGL = SkillAGL()
    languages: SkillINT = SkillINT()
    myths_and_legends: SkillINT = SkillINT()
    performance: SkillCHA = SkillCHA()
    persuasion: SkillCHA = SkillCHA()
    riding: SkillAGL = SkillAGL()
    seamanship: SkillINT = SkillINT()
    sleight_of_hand: SkillAGL = SkillAGL()
    sneaking: SkillAGL = SkillAGL()
    spot_hidden: SkillINT = SkillINT()
    swimming: SkillAGL = SkillAGL()

    axes: SkillSTR = SkillSTR()
    bows: SkillAGL = SkillAGL()
    brawling: SkillSTR = SkillSTR()
    crossbows: SkillAGL = SkillAGL()
    hammers: SkillSTR = SkillSTR()
    knives: SkillAGL = SkillAGL()
    slings: SkillAGL = SkillAGL()
    spears: SkillSTR = SkillSTR()
    staves: SkillAGL = SkillAGL()
    swords: SkillSTR = SkillSTR()

    secondary_skills: Dict[str, Skill]

    inventory: List[str] = Field(max_items=10)
    encumbrance_limit: int

    memento: str

    tiny_items: List[str]

    round_rest: bool = False
    stretch_rest: bool = False

    armor: str
    armor_rating: int
    armor_bane_on_sneaking: bool = False
    armor_bane_on_evade: bool = False
    armor_bane_on_acrobatics = False

    helmet: str
    helmet_rating: int
    helmet_bane_on_awareness: bool = False
    helmet_bane_on_ranged_attacks: bool = False

    willpower_points: int
    willpower_points_used: int = 0

    weapons: List[Weapon] = []

    hit_points: int
    hit_points_used: int = 0

    death_rolls_success: int = 0
    death_rolls_failures: int = 0


character_generator = BaseGenerator.load("dod_character_generator.yml")

if __name__ == '__main__':
    print(Character.schema_json(indent=2))
    print(character_generator.generate(
        Character.construct(kin="Wolfkin", age="Young", name="Greger")))
