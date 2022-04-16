import pytest
from args.exception import MultiParamError, ParamTypeError, ParamEnoughError
from args import parser
from args.parser import ListOptions, SingleOptions


def test_parser():
    options = parser.args_parser(['-l', '-p', '8080', '-d', '/usr/logs'], SingleOptions)
    assert options.l is True
    assert options.port == 8080
    assert options.directory == '/usr/logs'


@pytest.mark.parametrize('attr_name,example,excepted_value', [
    ('l', ['-l'], True),
    ('directory', ['-d', '/user/log'], '/user/log'),
    ('port', ['-p', '8080'], 8080),
])
def test_single_option_parser_set_flag_to_correct_value(attr_name, example, excepted_value):
    options = parser.args_parser(example, SingleOptions)
    value = getattr(options, attr_name)
    assert value == excepted_value


@pytest.mark.parametrize('attr_name,excepted_default', [
    ('l', False),
    ('directory', ''),
    ('port', 0),
])
def test_single_option_parser_not_set_flag_to_default_value(attr_name, excepted_default):
    options = parser.args_parser([], SingleOptions)
    value = getattr(options, attr_name)
    assert value == excepted_default


@pytest.mark.parametrize('flag,error_values', [
    ('-l', ['d']),
    ('-d', ['/user/log', '/tmp/log']),
    ('-p', ['8080', '8090']),
])
def test_single_option_parser_set_flag_to_multi_value_raise_error(flag, error_values):
    error_example = [flag] + error_values
    with pytest.raises(MultiParamError) as e:
        parser.args_parser(error_example, SingleOptions)
    assert e.value.flag == flag
    assert e.value.value == error_values


@pytest.mark.parametrize('flag,error_example,error_values', [
    ('-d', ['-l', '-d'], []),
    ('-p', ['-l', '-p'], []),
])
def test_single_option_parser_not_set_flag_enough_value_raise_error(
        flag, error_example, error_values):
    with pytest.raises(ParamEnoughError) as e:
        parser.args_parser(error_example, SingleOptions)
        assert e.value.flag == flag
        assert e.value.value == []


# TODO -p sad path ['-p','a']
def test_parser_set_p_to_str_raise_error():
    with pytest.raises(ParamTypeError) as e:
        parser.args_parser(['-p', 'a'], SingleOptions)
    assert e.value.flag == '-p'
    assert e.value.value == ['a']


@pytest.mark.parametrize('attr_name,example,excepted_value', [
    ('g', ['-g', 'this', 'is', 'a', 'list'], ['this', 'is', 'a', 'list']),
    ('d', ['-d', '1', '2', '-3', '4'], [1, 2, -3, 4]),
])
def test_list_option_parser_set_flag_to_correct_value(attr_name, example, excepted_value):
    options = parser.args_parser(example, ListOptions)
    value = getattr(options, attr_name)
    assert value == excepted_value


@pytest.mark.parametrize('attr_name,excepted_default', [
    ('g', []),
    ('d', []),
])
def test_list_option_parser_not_set_flag_to_default_value(attr_name, excepted_default):
    options = parser.args_parser([], ListOptions)
    value = getattr(options, attr_name)
    assert value == excepted_default


def test_list_option_parser_set_d_incorrect_value():
    with pytest.raises(ParamTypeError) as e:
        parser.args_parser(['-d', '1', 'a', '2'], ListOptions)
    assert e.value.flag == '-d'
    assert e.value.value == ['a']
