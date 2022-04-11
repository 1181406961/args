from dataclasses import dataclass
from typing import List
from args.exception import MultiParamError


def check_flag(params, index):
    if index + 1 < len(params) and not params[index + 1].startswith('-'):
        raise MultiParamError(field='-l', value=True)
    return True


@dataclass
class Parser:
    l: bool = False
    port: int = 0
    directory: str = ''

    PARAM_MAP = {
        '-l': lambda params, index: {'l': True} if check_flag(params, index) else {},
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
    for index, flag in enumerate(params):
        get_value = Parser.PARAM_MAP.get(flag, None)
        if get_value:
            kwargs.update(get_value(params, index))
    return Parser(**kwargs)
