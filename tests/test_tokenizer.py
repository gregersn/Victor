from victor.interpreter import Tokenizer


def test_plus():
    tokenizer = Tokenizer("+")
    tokens = tokenizer.make_tokens()

    assert len(tokens) == 1
    assert tokens[0].type == 'PLUS'


def test_simple_die():
    tokenizer = Tokenizer("d6")

    tokens = tokenizer.make_tokens()
    assert len(tokens) == 1
    assert tokens[0].type == 'DIEROLL'
    assert tokens[0].value == 'D6'


def test_multi_die():
    tokenizer = Tokenizer("3d6")
    tokens = tokenizer.make_tokens()
    assert len(tokens) == 1
    assert tokens[0].type == "DIEROLL"
    assert tokens[0].value == "3D6"


def test_die_multiplied():
    tokenizer = Tokenizer("3D6 * 5")
    tokens = tokenizer.make_tokens()
    assert len(tokens) == 3
    assert tokens[0].type == "DIEROLL"
    assert tokens[1].type == "MUL"
    assert tokens[2].type == "NUMBER"


def test_parenthesized_expression():
    tokenizer = Tokenizer("(2D6 + 6) * 5")
    tokens = tokenizer.make_tokens()
    assert len(tokens) == 7
    assert tokens[0].type == "LPAREN"
    assert tokens[1].type == "DIEROLL"
    assert tokens[2].type == "PLUS"
    assert tokens[3].type == "NUMBER"
    assert tokens[4].type == "RPAREN"
    assert tokens[5].type == "MUL"
    assert tokens[6].type == "NUMBER"


def test_variable_reference():
    tokenizer = Tokenizer("($SIZ + $CON) // 10 + $Mixed_Case_With_Underscore")
    tokens = tokenizer.make_tokens()
    assert len(tokens) == 9
    assert tokens[0].type == "LPAREN"

    assert tokens[1].type == "REFERENCE"
    assert tokens[1].value == 'SIZ'

    assert tokens[2].type == "PLUS"

    assert tokens[3].type == "REFERENCE"
    assert tokens[3].value == 'CON'

    assert tokens[4].type == "RPAREN"

    assert tokens[5].type == "IDIV"

    assert tokens[6].type == "NUMBER"
    assert tokens[6].value == 10

    assert tokens[7].type == 'PLUS'
    assert tokens[8].type == 'REFERENCE'


def test_conditional():
    tokenizer = Tokenizer("if 1 then 2 else 3")
    tokens = tokenizer.make_tokens()
    assert len(tokens) == 6
    assert tokens[0].type == "RESERVED"
    assert tokens[0].value == "IF"

    assert tokens[1].type == "NUMBER"
    assert tokens[2].type == "RESERVED"
    assert tokens[2].value == "THEN"

    assert tokens[3].type == "NUMBER"
    assert tokens[4].type == "RESERVED"
    assert tokens[4].value == "ELSE"

    assert tokens[5].type == "NUMBER"


def test_variable_assignment():
    tokenizer = Tokenizer("Foo: 1")
    tokens = tokenizer.make_tokens()
    assert len(tokens) == 3

    assert tokens[0].type == "ID"
    assert tokens[1].type == "ASSIGN"
    assert tokens[2].type == "NUMBER"


def test_variable_assign_string():
    tokenizer = Tokenizer("name: \"Foo\"")
    tokens = tokenizer.make_tokens()
    assert len(tokens) == 3
    assert tokens[0].type == "ID"
    assert tokens[1].type == "ASSIGN"
    assert tokens[2].type == "STRING"


def test_program():
    tokenizer = Tokenizer("Foo: 1\n1 + 2")
    tokens = tokenizer.make_tokens()
    assert len(tokens) == 7

    assert tokens[0].type == "ID"
    assert tokens[1].type == "ASSIGN"
    assert tokens[2].type == "NUMBER"
    assert tokens[3].type == "NEWLINE"
    assert tokens[4].type == "NUMBER"
    assert tokens[5].type == "PLUS"
    assert tokens[6].type == "NUMBER"
