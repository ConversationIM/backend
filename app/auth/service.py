import jwt
import datetime
from app import config
from app.common import exceptions

class AuthService(object):
	"""
	Handles operations related to authentication
	"""

	_secret = config.SECRET_KEY
	_params = config.JWT_PARAMS
	
	AUTH_HEADER_KEY = "Authorization"

	def __init__(self):
		pass
	
	def extract_token(self, request):
		return request.headers.get(self.AUTH_HEADER_KEY)

	def make_token(self, user):
		payload = {
				'sub': user.id,
				'email': user.email,
				'exp': datetime.datetime.utcnow() + datetime.timedelta(days=self._params['EXPIRATION_IN_DAYS'])
			}


		return jwt.encode(payload, self._secret, algorithm=self._params['ALGORITHM'])

	def validate_token(self, token):
		try:
			payload = jwt.decode(token, self._secret, algorithms=[self._params['ALGORITHM']])
			return payload
		except jwt.DecodeError:
			message = 'The provided token was invalid'
			raise exceptions.TokenValidationException(message)
		except jwt.InvalidTokenError:
			message = 'The provided token could not be decoded'
			raise exceptions.TokenValidationException(message)
