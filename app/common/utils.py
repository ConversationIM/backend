from flask import make_response as respond
from flask.json import dumps
import inflection

def make_response(data):
    """
    A version of flask's jsonify
    """
    response = { "meta": None, "data": data }

    response = respond((dumps(response), 200))
    response.headers['Content-Type'] = 'application/json'
    return response

def make_error(error):
    response = { "meta": None, "errors": [error.to_dict()]}

    response = respond((dumps(response), error.status))
    response.headers['Content-Type'] = 'application/json'
    return response

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
