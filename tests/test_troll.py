from victor.interpreter import get_interpreter


def test_single_die():
    i = get_interpreter()

    res = i.interpret("d6")

    assert res[0] == 0
    assert isinstance(res[1][0], int)


def test_multiple_dice():
    i = get_interpreter()
    res = i.interpret("3d6")

    assert res[0] == 0
    assert isinstance(res[1][0], list), res[1][0]
    assert len(res[1][0]) == 3, res[1][0]

    res = i.interpret(average=True)
    assert res[0] == 0
    assert res[1][0] == 10.5

    res = i.interpret("(4+1)d6")
    assert res[0] == 0
    assert isinstance(res[1][0], list), res[1][0]
    assert len(res[1][0]) == 5, res[1][0]

    res = i.interpret("(d4)d6")
    assert res[0] == 0
    assert isinstance(res[1][0], list), res[1][0]
    assert len(res[1][0]) >= 1, res[1][0]
    assert len(res[1][0]) <= 4, res[1][0]


def test_sum():
    i = get_interpreter()
    res = i.interpret("sum 3d6")

    assert res[0] == 0
    assert isinstance(res[1][0], int)
    assert res[1][0] >= 3
    assert res[1][0] <= 18
