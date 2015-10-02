from app.common.utils import depythonize

class Serializable(object):
    __public__ = None

    def to_dict(self):
        dict = {}
        for public_key in self.__public__:
            value = getattr(self, public_key)
            if value:
                public_key = depythonize(public_key)
                dict[public_key] = value
        return dict
