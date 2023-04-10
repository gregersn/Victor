kin_selection = {
    '1-4': 'Human',
    '5-7': 'Halfling',
    '8-9': 'Dwarf',
    '10': 'Elf',
    '11': 'Mallard',
    '12': 'Wolfkin'
}

$.kin = random_table(kin_selection)
$.abilities = table_lookup(abilities, $.kin)
$.profession = random_table(profession)
$.age = random_table(age)
$.name = random_table(name.get($.kin))
$.['STR', 'CON', 'AGL', 'INT', 'WIL', 'CHA'] = roll("sum largest 3 4d6")
swap(max($.['STR', 'CON', 'AGL', 'INT', 'WIL', 'CHA']), $.`table_lookup(key_attribute, $.profession)`)
$.movement = table_lookup(kin_movement, $.kin) + ranged_table(agility_movement, $.AGL)
$.damage_bonus_strength = ranged_table(damage_bonus, $.STR)
$.damage_bonus_agility = ranged_table(damage_bonus, $.AGL)
$.hit_points = $.CON
$.willpower_points = $.WIL
