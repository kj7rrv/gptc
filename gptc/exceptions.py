class GPTCError(BaseException):
    pass

class ModelError(GPTCError):
    pass

class UnsupportedModelError(ModelError):
    pass
