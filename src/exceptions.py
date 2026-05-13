class CrossModelExceptions(BaseException):
    def __init__(self, message, description=None):
        self.message = message
        self.description = description
