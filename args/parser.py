from dataclasses import dataclass
from typing import List
from functools import partial
from args.exception import MultiParamError


@dataclass
class OptionParser(object):
    params: List[str]
    index: int
    flag: str

    def parse_value(self):
        if self.index + 1 == len(self.params):
            return []
        end = self.index + 1
        while end < len(self.params):
            if self.params[end].startswith('-'):
                break
            end += 1
        return self.params[self.index + 1:end]

    def bool(self):
        values = self.parse_value()
        if len(values) != 0:
            raise MultiParamError(flag=self.flag, value=True)
        return True

    def single(self):
        values = self.parse_value()
        if len(values) != 1:
            raise MultiParamError(flag=self.flag, value=values)
        return values[0]


@dataclass
class Parser:
    l: bool = False
    port: int = 0
    directory: str = ''

    PARAM_MAP = {
        '-l': lambda params, index: {'l': OptionParser(params, index=index, flag='-l').bool()},
        '-p': lambda params, index: {'port': int(OptionParser(params, index=index, flag='-p').single())},
        '-d': lambda params, index: {'directory': OptionParser(params, index=index, flag='-d').single()},
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
    list(map(partial(parser_flag_value, params=params, kwargs=kwargs), range(len(params))))
    return Parser(**kwargs)


def parser_flag_value(index, params, kwargs):
    get_value = Parser.PARAM_MAP.get(params[index], None)
    if get_value:
        kwargs.update(get_value(params, index))
