from pathlib import Path
from victor.render.field_mapping import remap_reverse, get_value


def test_get_value():
    val = get_value({'foo': {'bar': 1}}, 'foo.bar'.split('.'))
    assert val == 1


def test_remap_reverse():
    character_data = Path('examples/coc_7e_character_data.yaml')
    mapping_schema = Path("examples/coc_7e_sheet_reverse_mapping.yaml")
    field_values = remap_reverse(values=character_data,
                                 schema=mapping_schema)['fields']

    assert field_values['Investigator_Name'] == "Arthur Knowles"
    assert field_values['Skill_Dodge'] == 52
    assert field_values['SkillDef_ArtCraft1'] == "Photography"
    assert field_values['Skill_ArtCraft1'] == 5
    assert field_values['Skill_Dodge_half'] == 26
    assert field_values['Skill_Dodge_fifth'] == 10
    assert field_values['Skill_ArtCraft1_half'] == 2
    assert field_values['Skill_ArtCraft1_fifth'] == 1
