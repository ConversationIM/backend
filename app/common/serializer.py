from app.common import language

class Serializable(object):
    __public__ = None

    def to_dict(self):
        dict = {}
        for public_key in self.__public__:
            value = getattr(self, public_key)
            if value:
                public_key = language.depythonize(public_key)
                dict[public_key] = value
        return dict
