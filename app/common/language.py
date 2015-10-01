import inflection

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
