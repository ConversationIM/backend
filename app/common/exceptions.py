class ValidationException(Exception):
    """
    An exception indicating that an error 
    occurred during validation. 
    """
    
    def __init__(self, message, field):
        """
        Initializes the error
        :field the String value of the field that caused the error
        """
        
        self.field = field
        super(ValidationException, self).__init__(message)