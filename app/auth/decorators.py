import functools
from json import loads
from flask import request
from app.common import errors, exceptions, utils
from app.auth.service import AuthService

def authenticated_request(f):
    """
    Ensures that an incoming request provides a valid
    authentication token
    """

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        auth_service = AuthService()
        auth_token = auth_service.extract_token(request)
        if not auth_token:
            message = "This resource cannot be accessed without a valid authentication token"
            source = auth_service.AUTH_HEADER_KEY
            return utils.make_error(errors.UnauthenticatedRequestError(message, source))

        payload = None
        try:
            payload = auth_service.validate_token(auth_token)
        except exceptions.TokenValidationException, e:
            message = e.message
            source = auth_service.AUTH_HEADER_KEY
            return utils.make_error(errors.UnauthenticatedRequestError(message, source))

        kwargs['user'] = payload
        return f(*args, **kwargs)
    return wrapped

def authenticated_event(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        data = args[0] if len(args) else None
        auth_token = None
        if data:
            data = loads(data)
            auth_token = data.get('token')
            kwargs['data'] = data

        if not auth_token:
            message = "This resource cannot be accessed without a valid authentication token"
            kwargs['error'] = message
        else:
            auth_service = AuthService()
            try:
                payload = auth_service.validate_token(auth_token)
                kwargs['user'] = payload
            except exceptions.TokenValidationException, e:
                message = e.message
                kwargs['error'] = message

        return f(*args, **kwargs)
    return wrapped
