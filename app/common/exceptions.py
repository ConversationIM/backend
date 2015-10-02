class ValidationException(Exception):
    def __init__(self, message, field):
        self.field = field
        super(ValidationException, self).__init__(message)