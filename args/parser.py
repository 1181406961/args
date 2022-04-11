from dataclasses import dataclass
from typing import List
from args.exception import ParamError


def check_param(params, index, need_check):
    if need_check == '-l':
        if index+1 < len(params) and not params[index + 1].startswith('-'):
            raise ParamError(field=need_check, value=True)
    return True


@dataclass
class Parser:
    l: bool = False
    port: int = 0
    directory: str = ''

    PARAM_MAP = {
        '-l': lambda params, index: {'l': True},
        '-p': lambda params, index: {'port': int(params[index + 1])},
        '-d': lambda params, index: {'directory': params[index + 1]},
    }


def args_parser(params: List[str]):
    '''
    传入参数进行解析
    :param params:
    :return:
    '''

    kwargs = {}
    if not params:
        return Parser()
    for index, param in enumerate(params):
        get_value = Parser.PARAM_MAP.get(param, None)
        if get_value and check_param(params=params, index=index, need_check=param):
            kwargs.update(get_value(params, index))
    return Parser(**kwargs)
