
class ParamError(ValueError):
    def __init__(self, field, value):
        self.field = field
        self.value = value
