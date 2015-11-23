class ValidationException(Exception):
    """
    An exception indicating that an error 
    occurred during model validation. 
    """
    
    def __init__(self, message, field):
        """
        Initializes the error
        :field the String value of the field that caused the error
        """
        
        self.field = field
        super(ValidationException, self).__init__(message)

class TokenValidationException(Exception):
	"""
	An exception indicating that an error
	occurred during token validation.
	"""

	def __init__(self, message):
		super(TokenValidationException, self).__init__(message)    
                
class InvalidOperationException(Exception):
    """
    An exception indicating that the
    requested operation is not possible now,
    but may be possible later
    """
    
    def __init__(self, message):
        super(TokenValidationException, self).__init__(message)  