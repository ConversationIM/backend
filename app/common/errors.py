from app.common.mixins import general

class _BaseError(general.Serializable):

    __public__ = ['type', 'message', 'status', 'code', 'source']

    def __init__(self, type, message, status, code, source):
        self.type = type
        self.message = message
        self.status = status
        self.code = code
        self.source = source
        self.acknowledgable = True

class InvalidParameterError(_BaseError):

    def __init__(self, message, source):
        type = 'InvalidParameterError'
        if message is None:
            message = 'One or more parameters in the request were invalid'
        status = 400
        code = 101

        super(InvalidParameterError, self).__init__(type, message, status, code, source)

class ApiError(_BaseError):

    def __init__(self):
        type = 'ApiError'
        message = 'Something went wrong while processing that request'
        status = 500
        code = 100

        super(ApiError, self).__init__(type, message, status, code, None)
