
class MultiParamError(ValueError):
    def __init__(self, flag, value):
        self.flag = flag
        self.value = value
