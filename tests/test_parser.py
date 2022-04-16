import pytest
from args.exception import MultiParamError, ParamTypeError
from args import parser


# TODO ['-l', '-p', '8080', '-d', '/usr/logs'] 传一个列表可以解析
def test_parser():
    p = parser.args_parser(['-l', '-p', '8080', '-d', '/usr/logs'])
    assert p.l is True
    assert p.port == 8080
    assert p.directory == '/usr/logs'


# TODO -l 为True
def test_parser_set_l_to_true():
    p = parser.args_parser(['-l'])
    assert p.l is True


# TODO -l sad path ['-l' 'abc']
def test_parser_set_l_to_multi_params():
    with pytest.raises(MultiParamError) as e:
        parser.args_parser(['-l', '/user/log'])
    assert e.value.flag == '-l'


#   TODO default 为False
def test_parser_not_set_l_to_false():
    p = parser.args_parser([])
    assert p.l is False


# TODO -p 为端口
def test_parser_set_p_to_port():
    p = parser.args_parser(['-p', '8080'])
    assert p.port == 8080


# TODO -p sad path ['-p','8080','8090']
def test_parser_set_p_to_multi_port_raise_error():
    with pytest.raises(MultiParamError) as e:
        parser.args_parser(['-p', '8080', '8090'])
    assert e.value.flag == '-p'
    assert e.value.value == ['8080', '8090']


# TODO -p sad path ['-p','a']
def test_parser_set_p_to_str_raise_error():
    with pytest.raises(ParamTypeError) as e:
        parser.args_parser(['-p', 'a'])
    assert e.value.flag == '-p'
    assert e.value.value == ['a']


#   TODO default 为0
def test_parser_not_set_p_to_zero():
    p = parser.args_parser([])
    assert p.port == 0


# TODO -d 为目录
def test_parser_set_d_to_directory():
    p = parser.args_parser(['-d', '/user/log'])
    assert p.directory == '/user/log'


# TODO -d sad path ['-d','/user/log','/user/tmp']
def test_parser_set_d_to_multi_directory_raise_error():
    with pytest.raises(MultiParamError) as e:
        parser.args_parser(['-d', '/user/log', '/user/asd'])
    assert e.value.flag == '-d'
    assert e.value.value == ['/user/log', '/user/asd']


#   TODO default 为""
def test_parser_not_set_d_to_empty_str():
    p = parser.args_parser([])
    assert p.directory == ''


# TODO -g ['this','is','a','list']
def test_parser_g_set_multi_value():
    p = parser.args_parser(['-g', 'this', 'is', 'a', 'list'])
    assert p.g == ['this', 'is', 'a', 'list']


# TODO -d default 为[]
def test_parser_not_set_g_to_empty_list():
    p = parser.args_parser([])
    assert p.g == []
