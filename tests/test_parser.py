import pytest
from args.exception import MultiParamError
from args.parser import args_parser


# TODO ['-l', '-p', '8080', '-d', '/usr/logs'] 传一个列表可以解析
def test_parser():
    parser = args_parser(['-l', '-p', '8080', '-d', '/usr/logs'])
    assert parser.l is True
    assert parser.port == 8080
    assert parser.directory == '/usr/logs'


# TODO -l 为True
def test_parser_set_l_to_true():
    parser = args_parser(['-l'])
    assert parser.l is True


# TODO -l sad path ['-l' 'abc']
def test_parser_set_l_to_multi_params():
    with pytest.raises(MultiParamError) as e:
        args_parser(['-l', '/user/log'])
    assert e.value.flag == '-l'


#   TODO default 为False
def test_parser_not_set_l_to_false():
    parser = args_parser([])
    assert parser.l is False


# TODO -p 为端口
def test_parser_set_p_to_port():
    parser = args_parser(['-p', '8080'])
    assert parser.port == 8080


# TODO -p sad path ['-p','8080','8090']
def test_parser_set_p_to_multi_port():
    with pytest.raises(MultiParamError) as e:
        args_parser(['-p', '8080', '8090'])
    assert e.value.flag == '-p'
    assert e.value.value == ['8080', '8090']


#   TODO default 为0
def test_parser_not_set_p_to_zero():
    parser = args_parser([])
    assert parser.port == 0


# TODO -d 为目录
def test_parser_set_d_to_directory():
    parser = args_parser(['-d', '/user/log'])
    assert parser.directory == '/user/log'


# TODO -d sad path ['-d','/user/log','/user/tmp']
def test_parser_set_d_to_multi_directory():
    with pytest.raises(MultiParamError) as e:
        parser = args_parser(['-d', '/user/log', '/user/asd'])
    assert e.value.flag == '-d'
    assert e.value.value == ['/user/log', '/user/asd']


#   TODO default 为""
def test_parser_not_set_d_to_empty():
    parser = args_parser([])
    assert parser.directory == ''
