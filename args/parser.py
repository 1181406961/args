from typing import List, Callable, Any, Optional
from functools import partial, cached_property
from args.exception import MultiParamError, ParamTypeError, ParamEnoughError


class OptionParser:
    def __init__(self, *,
                 flag: str,
                 default: Optional[Any],
                 get_value: Callable,
                 excepted_size: Optional[int] = None,
                 type: Callable = str):
        self.change_to = type
        self.excepted_size = excepted_size
        self.flag = flag
        self.default = default
        self.get_flag_value = get_value

    def __set_name__(self, owner: 'Parser', name: str):
        self.public_name = name
        self.private_name = f'_{name}'

    def __get__(self, instance: 'Parser', owner: 'Parser'):
        if not hasattr(instance, self.private_name):
            return self.default
        return getattr(instance, self.private_name)

    def __set__(self, instance: 'Parser', value: Any):
        setattr(instance, self.private_name, value)

    def values(self, params: List[str]):
        i = 0
        while i < len(params):
            if params[i] == self.flag:
                break
            i += 1
        if i + 1 == len(params):
            return []
        end = i + 1
        while end < len(params):
            if params[end].startswith('-'):
                break
            end += 1
        return params[i + 1:end]

    def parser_attr(self, params: List[str]):
        values = self.values(params)
        if self.excepted_size is None:
            return self.get_flag_value(self.change_values_type(values))
        if len(values) > self.excepted_size:
            raise MultiParamError(flag=self.flag, value=values)
        elif len(values) < self.excepted_size:
            raise ParamEnoughError(flag=self.flag, value=values)
        return self.get_flag_value(self.change_values_type(values))

    def change_values_type(self, values: List[str]):
        error_type_values = []
        result = []
        for value in values:
            try:
                result.append(self.change_to(value))
            except ValueError:
                error_type_values.append(value)
        if error_type_values:
            raise ParamTypeError(flag=self.flag, value=error_type_values)
        return result


def get_single_value(values: List[Any]):
    return values[0]


class Parser:
    l = OptionParser(type=bool, excepted_size=0, flag='-l', default=False, get_value=lambda values: True)
    port = OptionParser(type=int, excepted_size=1, flag='-p', default=0, get_value=get_single_value)
    directory = OptionParser(excepted_size=1, flag='-d', default='', get_value=get_single_value)
    g = OptionParser(flag='-g', default=[], get_value=lambda values: values)

    def parser(self, flag: str, params: List[str]):
        flag_map_fields = self.flag_map_fields
        field = flag_map_fields.get(flag, None)
        if field:
            setattr(self, field.public_name, field.parser_attr(params))

    @cached_property
    def flag_map_fields(self):
        class_attrs = self.__class__.__dict__
        flag_map_fields = {}
        for key in class_attrs:
            field = class_attrs[key]
            if isinstance(field, OptionParser):
                flag_map_fields[field.flag] = field
        return flag_map_fields


def args_parser(params: List[str]):
    '''
    传入参数进行解析
    :param params:
    :return:
    '''

    option = Parser()
    list(map(partial(option.parser, params=params), params))
    return option
