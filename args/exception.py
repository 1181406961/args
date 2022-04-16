class ParamError(ValueError):
    def __init__(self, flag, value):
        self.flag = flag
        self.value = value


class MultiParamError(ParamError):
    pass


class ParamTypeError(ParamError):
    pass
