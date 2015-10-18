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

	def __init__(self):
		pass

	def make_token(self, user):
		payload = {
				'sub': user.id,
				'email': user.email,
				'exp': datetime.datetime.utcnow() + datetime.timedelta(days = self._params['EXPIRATION_IN_DAYS'])
			}


		return jwt.encode(payload, self._secret, algorithm=self._params['ALGORITHM'])

	def validate_token(self, token):
		try:
			payload = jwt.decode(token, algorithms=[self._params['ALGORITHM']])
		except jwt.DecodeError:
			message = 'The provided token is invalid'
			raise exceptions.TokenValidationExeception(message)
		except jwt.InvalidTokenError:
			message = 'The provided token could not be decoded'
			raise exceptions.TokenValidationExeception(message)
