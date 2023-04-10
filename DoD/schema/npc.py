from typing import Literal
from pydantic import Field
from schema.common import Kin, Profession
from schema.sheet import BaseSheet, random_table

Attitude = Literal['Hostile', 'Evasive', 'Indifferent', 'Friendly']

Motivation = Literal['Sweet, glittering gold', 'Knoledge of the world',
                     'Deep and eternal love', 'A lifelong oath',
                     'An injustice that demands retribution',
                     'A life of joy and song',
                     'Blood ties that can never be severed',
                     'Escaping a dark past']


Trait = Literal['Talks too much', 'Strange clothes', 'Wild-eyed', 'Smells bad', 'Joker',
                'Cultist',
                'A bit childish', 'Quit and difficult', 'Demon worshiper', 'Obstinate',
                'Very touchy', 'Highly romantic']

NPCName = [['Agnar', 'Jorid', 'Dareios'], ['Ragnfast', 'Ask', 'Xanthos'],
           ['Arnulf', 'Tyra', 'Xanthos'], ['Atle', 'Liv', 'Athalia'],
           ['Guthorm', 'Embla', 'Kleitos'], ['Botvid', 'Ragna', 'Astara'],
           ['Kale', 'Turid', 'Priamus'], ['Egil', 'Jorunn', 'Galyna'],
           ['Ingemund', 'Borghild', 'Taras'], ['Gudmund', 'Gylla', 'Zenais'],
           ['Grim', 'Tora', 'Hesiod'], ['Brand', 'Edda', 'Liene'],
           ['Folkvid', 'Sigrun', 'Eupraxia'], ['Germund', 'Dagrun', 'Taras'],
           ['Algot', 'Bolla', 'Lysandra'], ['Tolir', 'Yrsa', 'Kalias'],
           ['Hjorvald', 'Estrid', 'Isidora'], ['Ambjorn', 'Signe', 'Athos'],
           ['Grunn', 'Tilde', 'Larysa'], ['Olgrid', 'Idun', 'Nikias']
           ]


class NPC(BaseSheet):
    name: str = Field(
        name='name', default_factory=lambda: random_table(NPCName))
    kin: Kin
    profession: Profession
    attitude: Attitude
    motivation: Motivation
    trait: Trait
