def route(self, *args, **kwargs):
    """
    Flask Snippet #129
    http://flask.pocoo.org/snippets/129/
    """
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper
