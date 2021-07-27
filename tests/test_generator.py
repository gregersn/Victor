from victor import generate


def test_generate_guff():
    monster = generate("./examples/guff.md", average=True)

    assert monster.variables['Name'] == 'Guff'
    assert monster.variables['STR'] == 47.5

    assert monster.variables['HitPoints'] == 14
    assert monster.variables['MagicPoints'] == 27
