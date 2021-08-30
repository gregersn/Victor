from victor.interpreter import get_interpreter


def test_single_die():
    for i in range(0, 20):
        expression = f"d{i}"
        interpreter = get_interpreter(expression)
        res = interpreter.interpret(average=True)
        assert res[0] == 0
        if i > 1:
            assert res[1][0] == (1 + i) / 2, expression
        else:
            assert res[1][0] == i, expression

        for _ in range(0, 100):
            res = interpreter.interpret()
            assert res[0] == 0, expression
            assert res[1][0] >= min(1, i), expression
            assert res[1][0] <= i, expression


def test_dice_pool():
    expression = "4d6"

    interpreter = get_interpreter(expression)
    res = interpreter.interpret()
    assert res[0] == 0
    assert isinstance(res[1][0], list)
    assert len(res[1][0]) == 4


def test_dice_pool_keep():
    # http://hjemmesider.diku.dk/~torbenm/Troll/Troll-SAC.pdf
    expression = "largest 3 4d6"


"""
d6 - single die roll
3d6 - list of die rolls
sum 3d6 - sum of list of die rolls
max 4d10 - largest of 4 dice
sum largest 3 4d6

"""
