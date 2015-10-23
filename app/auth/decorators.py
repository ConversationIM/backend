import functools
from json import loads
from flask import request
from app.common import errors, exceptions, utils
from app.auth.service import AuthService

def authenticated_request(f):
    """
    Ensures that an incoming request provides a valid
    authentication token
    TODO: Test to ensure functionality works
    """
    
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        auth_service = AuthService()
        auth_token = auth_service.extract_token(request)
        if not auth_token:
            message = "This resource cannot be accessed without a valid authentication token"
            source = auth_service.AUTH_HEADER_KEY
            return utils.make_error(errors.MissingParameterError(message, source))
        
        payload = None
        try:
            payload = auth_service.validate_token(auth_token)
        except exceptions.TokenValidationExeception, e:
            message = e.message
            source = auth_service.AUTH_HEADER_KEY
            return utils.make_error(errors.InvalidParameterError(message, source))
        
        kwargs['user'] = payload
        return f(*args, **kwargs)
    return wrapped

def authenticated_event(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        auth_service = AuthService()
        
        data = args['data']
        auth_token = None
        if data:
            data = loads(data)
            auth_token = data['token']
            kwargs['data'] = data
            
        if not auth_token:
            message = "This resource cannot be accessed without a valid authentication token"
            kwargs['error'] = message
        
        payload = None
        try:
            payload = auth_service.validate_token(auth_token)
            kwargs['user'] = payload
        except exceptions.TokenValidationExeception, e:
            message = e.message
            kwargs['error'] = message
        
        return f(*args, **kwargs)
    return wrapped