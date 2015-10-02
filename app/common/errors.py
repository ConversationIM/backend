from app.common.mixins import general

class _BaseError(general.Serializable):

    __public__ = ['type', 'message', 'code', 'source']

    def __init__(self, type, message, status, code, source):
        if source and not isinstance(source, list):
            raise TypeError("Error source must be a list")

        self.acknowledgable = True
        self.type = type
        self.message = message
        self.status = status
        self.code = code

        if source is None:
            self.source = []
        else:
            self.source = source

class InvalidParameterError(_BaseError):

    def __init__(self, message, source):
        type = 'InvalidParameterError'
        if not message:
            message = 'One or more parameters in the request were invalid'
        status = 400
        code = 102

        super(InvalidParameterError, self).__init__(type, message, status, code, source)

class MissingParameterError(_BaseError):

    def __init__(self, message, source):
        type = 'MissingParameterError'
        if not message:
            message = 'One or more parameters were missing from the request'
        status = 400
        code = 101

        super(MissingParameterError, self).__init__(type, message, status, code, source)

class ApiError(_BaseError):

    def __init__(self):
        type = 'ApiError'
        message = 'Something went wrong while processing that request'
        status = 500
        code = 100

        super(ApiError, self).__init__(type, message, status, code, None)
