from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Callable, Any, Optional
from functools import partial
from args.exception import MultiParamError


class Field(ABC):
    def __init__(self, flag: str, default: Optional[Any], get: Callable):
        self.flag = flag
        self.default = default
        self.get = get

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f'_{name}'

    def __get__(self, instance, owner):
        if not hasattr(instance, self.private_name):
            return self.default
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        setattr(instance, self.private_name, value)

    def values(self, params):
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

    @abstractmethod
    def parser_attr(self, params):
        '''
        :param params:
        :return:
        '''


class SingleField(Field):
    def __init__(self, value_size: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value_size = value_size

    def parser_attr(self, params):
        values = self.values(params)
        if len(values) != self.value_size:
            raise MultiParamError(flag=self.flag, value=values)
        return self.get(values)


class Option:
    l = SingleField(value_size=0, flag='-l', default=False, get=lambda values: True)
    port = SingleField(value_size=1, flag='-p', default=0, get=lambda values: int(values[0]))
    directory = SingleField(value_size=1, flag='-d', default='', get=lambda values: values[0])

    def parser(self, flag, params):
        flag_map_fields = self.flag_map_fields()
        field = flag_map_fields.get(flag, None)
        if field:
            setattr(self, field.public_name, field.parser_attr(params))

    @classmethod
    def flag_map_fields(cls):
        if hasattr(cls, '_flag_map_fields'):
            return cls._flag_map_fields
        flag_map_fields = {}
        for key in cls.__dict__:
            value = cls.__dict__[key]
            if isinstance(value, Field):
                flag_map_fields[value.flag] = value
        cls._flag_map_fields = flag_map_fields
        return cls._flag_map_fields


def args_parser(params: List[str]):
    '''
    传入参数进行解析
    :param params:
    :return:
    '''

    option = Option()
    list(map(partial(option.parser, params=params), params))
    return option
