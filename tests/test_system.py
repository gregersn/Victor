from victor.interpreter import get_interpreter


def test_load_system():
    interpreter = get_interpreter("load_system(\"examples/testsystem.yml\")")
    res = interpreter.interpret()
    assert 'a_list' in interpreter.system_variables
    assert type(interpreter.system_variables['a_list']) == list
