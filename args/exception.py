class ParamError(ValueError):
    def __init__(self, flag, value):
        self.flag = flag
        self.value = value


class MultiParamError(ParamError):
    '''
    参数过多
    '''


class ParamTypeError(ParamError):
    '''
    参数类型错误
    '''


class ParamEnoughError(ParamError):
    '''
    参数不够
    '''
