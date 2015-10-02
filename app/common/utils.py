import app.common as common
from flask import make_response as respond
from flask import json
import inflection

def byteify(input):
    """
    See http://stackoverflow.com/a/13105359/996249
    """
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def make_response(data):
    response = { "meta": { 'status': 200 }, "data": data }

    response = respond((json.dumps(response), 200))
    response.headers['Content-Type'] = 'application/json'
    return response

def make_error(errors):
    error_list = []
    if type(errors) is not list:
        errors = [errors]
    for error in errors:
        error_list.append(error.to_dict())

    status = max(error.status for error in errors)
    response = { "meta": { 'status': status }, "errors": error_list }
    response = respond((json.dumps(response), status))
    response.headers['Content-Type'] = 'application/json'
    return response

def make_validation_error(validation_exception):
    message = validation_exception.message
    source = None
    if validation_exception.field:
        source = depythonize(validation_exception.field)
    
    return make_error(common.errors.InvalidParameterError(message, source))

def make_marshal_error(marshal_result):
    error = None
    if marshal_result[1]:
        message = None
        source = marshal_result[1]
        error = make_error(common.errors.MissingParameterError(message, source))

    return error

def marshal_request(arguments, expected):
    arguments = byteify(json.loads(arguments))
    required = expected.get('required', [])
    allowed = expected.get('allowed', [])

    marshalled_arguments = {}
    for key, value in arguments.iteritems():
        if (key in required or key in allowed):
            marshalled_arguments[key] = value

    missing = list(set(required) - set(marshalled_arguments.keys()))
    return (marshalled_arguments, missing)

def pythonize(word):
    return inflection.underscore(word)

def pythonize_dict(dictionary):
    new_dictionary = {}
    for key, value in dictionary.iteritems():
        key = inflection.underscore(key)
        new_dictionary[key] = value

    return new_dictionary

def depythonize(word):
    return inflection.camelize(word, False)

def depythonize_dict(dictionary):
    new_dictionary = {}
    for key, value in dictionary.iteritems():
        key = inflection.camelize(key, False)
        new_dictionary[key] = value

    return new_dictionary
