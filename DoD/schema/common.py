from enum import Enum


class Kin(str, Enum):
    human = 'Human'
    dwarf = 'Dwarf'
    elf = 'Elf'
    halfling = 'Halfling'
    wolfkin = 'Wolfkin'
    mallard = 'Mallard'


class Profession(Enum):
    bard = 'Bard'
    artisan = 'Artisan'
    hunter = 'Hunter'
    fighter = 'Fighter'
    scholar = 'Scholar'
    mage = 'Mage'
    merchant = 'Merchant'
    knight = 'Knight'
    mariner = 'Mariner'
    thief = 'Thief'
