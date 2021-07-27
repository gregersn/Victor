from victor.interpreter import interpret
from victor.interpreter import Interpreter, Tokenizer, Parser


def test_simple():
    res = interpret("1 + 2")
    assert res[0] == 0
    assert res[1][0] == 3


def test_die_roll():
    res = interpret("d6", average=True)
    assert res[0] == 0
    assert res[1][0] == 3.5

    for _ in range(100):
        res = interpret("d6", average=False)
        assert res[0] == 0
        assert res[1][0] >= 1
        assert res[1][0] <= 6
        assert isinstance(res[1][0], int)


def test_complex_die_roll():
    res = interpret("(2d6 + 6) * 5", average=True)
    assert res[0] == 0
    assert res[1][0] == 65

    res = interpret("(3d6+6)*5", average=True)
    assert res[0] == 0
    assert res[1][0] == 82.5


def test_unary():
    res = interpret("-4")
    assert res[1][0] == -4

    res = interpret("+3")
    assert res[1][0] == 3


def test_logical_boolean():
    res = interpret("2 < 3")
    assert res[1][0] is True

    res = interpret("2 > 3")
    assert res[1][0] is False


def test_conditional():
    res = interpret("if 1 then 3")
    assert res[1][0] == 3

    res = interpret("if 0 then 3")
    assert res[1][0] is None


def test_assignment():
    tokenizer = Tokenizer("Foo: 5")
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser)
    res = interpreter.interpret()
    assert res[1][0] == 5

    Foo = interpreter.variables.get('Foo')
    assert Foo is not None
    assert Foo == 5


def test_assign_string():
    tokenizer = Tokenizer("name: \"Somename\"")
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser)
    _ = interpreter.interpret()

    name = interpreter.variables.get('name')
    assert name == 'Somename'


def test_assignment_reference():
    res = interpret("Foo: 2\n$Foo + 5")
    assert res[1][0] == 2
    assert res[1][1] == 7
