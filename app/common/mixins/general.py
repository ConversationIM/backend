from app.common.utils import depythonize

class Serializable(object):
    """
    Provides an interface for basic object serialization.
    Implementers should extend this class and override
    __public__ with the fields that should be included in
    serialization
    """
    
    __public__ = None

    def to_dict(self):
        """
        Creates a dictionary containing the keys specified
        in __public__ and their associated values
        """
        
        dict = {}
        for public_key in self.__public__:
            value = getattr(self, public_key)
            if value:
                public_key = depythonize(public_key)
                dict[public_key] = value
        return dict
