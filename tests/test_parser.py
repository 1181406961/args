import pytest
from args.exception import MultiParamError, ParamTypeError, ParamEnoughError
from args import parser


def test_parser():
    p = parser.args_parser(['-l', '-p', '8080', '-d', '/usr/logs', '-g', 'this', 'is', 'a', 'list'])
    assert p.l is True
    assert p.port == 8080
    assert p.directory == '/usr/logs'
    assert p.g == ['this', 'is', 'a', 'list']


@pytest.mark.parametrize('attr_name,example,excepted_value', [
    ('l', ['-l'], True),
    ('directory', ['-d', '/user/log'], '/user/log'),
    ('port', ['-p', '8080'], 8080),
    ('g', ['-g', 'this', 'is', 'a', 'list'], ['this', 'is', 'a', 'list'])
])
def test_option_parser_set_flag_to_correct_value(attr_name, example, excepted_value):
    p = parser.args_parser(example)
    value = getattr(p, attr_name)
    assert value == excepted_value


@pytest.mark.parametrize('attr_name,excepted_default', [
    ('l', False),
    ('directory', ''),
    ('port', 0),
    ('g', [])
])
def test_option_parser_not_set_flag_to_default_value(attr_name, excepted_default):
    p = parser.args_parser([])
    value = getattr(p, attr_name)
    assert value == excepted_default


@pytest.mark.parametrize('flag,error_values', [
    ('-l', ['d']),
    ('-d', ['/user/log', '/tmp/log']),
    ('-p', ['8080', '8090']),
])
def test_option_parser_set_flag_to_multi_value_raise_error(flag, error_values):
    error_example = [flag] + error_values
    with pytest.raises(MultiParamError) as e:
        parser.args_parser(error_example)
    assert e.value.flag == flag
    assert e.value.value == error_values


@pytest.mark.parametrize('flag,error_example,error_values', [
    ('-d', ['-l', '-d'], []),
    ('-p', ['-l', '-p'], []),
])
def test_option_parser_not_set_flag_enough_value_raise_error(flag, error_example, error_values):
    with pytest.raises(ParamEnoughError) as e:
        parser.args_parser(error_example)
        assert e.value.flag == flag
        assert e.value.value == []


# TODO -p sad path ['-p','a']
def test_parser_set_p_to_str_raise_error():
    with pytest.raises(ParamTypeError) as e:
        parser.args_parser(['-p', 'a'])
    assert e.value.flag == '-p'
    assert e.value.value == ['a']
