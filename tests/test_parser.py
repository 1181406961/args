import pytest
from args.exception import ParamError
from args.parser import args_parser


# TODO ['-l', '-p', '8080', '-d', '/usr/logs'] 传一个列表可以解析
def test_parser():
    parser = args_parser(['-l', '-p', '8080', '-d', '/usr/logs'])
    assert parser.l is True
    assert parser.port == 8080
    assert parser.directory == '/usr/logs'


# TODO -l 为True
def test_parser_l_set_flag_to_true():
    parser = args_parser(['-l'])
    assert parser.l is True


# TODO sad path ['-l' 'abc']
def test_parser_l_after_has_no_param():
    with pytest.raises(ParamError) as e:
        args_parser(['-l', '/user/log'])
    assert e.value.field == '-l'


#   TODO default 为False
def test_parser_l_not_set_flag_to_false():
    parser = args_parser([])
    assert parser.l is False


# TODO -p 为端口
def test_parser_p_set_port():
    parser = args_parser(['-p', '8080'])
    assert parser.port == 8080


#   TODO default 为0
def test_parser_not_set_p_to_zero():
    parser = args_parser([])
    assert parser.port == 0


# TODO -d 为目录
def test_parser_set_d_to_directory():
    parser = args_parser(['-d', '/user/log'])
    assert parser.directory == '/user/log'


#   TODO default 为""
def test_parser_not_set_d_to_empty():
    parser = args_parser([])
    assert parser.directory == ''
