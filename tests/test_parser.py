from victor.interpreter import Parser
from victor.interpreter import Tokenizer
from victor.interpreter.ast import (
    BinOp, DieRoll, Number, Reference, UnaryOp, Assign,
    IfNode, Call)


def parse(prg: str) -> Parser:
    return Parser(Tokenizer(prg))


def test_dieroll():
    tokenizer = Tokenizer("3d6")
    parser = Parser(tokenizer)

    res = parser.factor()

    assert isinstance(res, DieRoll)
    assert res.value == "3D6"


def test_atoms():
    tokenizer = Tokenizer("5")
    parser = Parser(tokenizer)

    res = parser.atom()

    assert isinstance(res, Number)
    assert res.value == 5

    tokenizer = Tokenizer("$foo")
    parser = Parser(tokenizer)

    res = parser.atom()

    assert isinstance(res, Reference), res
    assert res.value == "foo", res.value

    tokenizer = Tokenizer("4d10")
    parser = Parser(tokenizer)

    res = parser.atom()

    assert isinstance(res, DieRoll), res
    assert res.value == "4D10", res.value

    tokenizer = Tokenizer("(6)")
    parser = Parser(tokenizer)

    res = parser.atom()

    assert isinstance(res, Number)
    assert res.value == 6


def test_factors():
    tokenizer = Tokenizer("-5")
    parser = Parser(tokenizer)
    res = parser.factor()

    assert isinstance(res, UnaryOp)
    assert isinstance(res.expr, Number)


def test_term():
    tokenizer = Tokenizer("5 * 6")
    parser = Parser(tokenizer)
    res = parser.term()

    assert isinstance(res, BinOp)
    assert res.op.type == 'MUL'


def test_comparative_expr():
    res = parse("5 < 6").comparative_expr()

    assert isinstance(res, BinOp)
    assert res.op.type == 'LESSTHAN'


def test_arithmetic_expr():
    res = parse("4 + 9").arithmetic_expr()

    assert isinstance(res, BinOp)
    assert res.op.type == 'PLUS'


def test_assignment_expr():
    res = parse("Foo: 1").expr()

    assert isinstance(res, Assign)


def test_assignment_string_expr():
    res = parse("name: \"Foobar\"").expr()

    assert isinstance(res, Assign)


def test_multiline_expr():
    res = parse("Foo: 1\n1 + 2").rule_program()
    assert isinstance(res, list), res


def test_if_else_with_logic():
    res = parse("if 1 < 2 and 3 < 2 then 1 else 2").conditional_expr()
    assert isinstance(res, IfNode)


def test_builtin_function_max():
    res = parse("max(2, 4)").function_call()
    assert isinstance(res, Call), res

    res = parse("max(3, 1)").function_call()
    assert isinstance(res, Call), res

    res = parse("max(2, 4, 3, 5)").function_call()
    assert isinstance(res, Call), res
