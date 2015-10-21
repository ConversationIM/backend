from app.common import utils, errors
from app.users.service import UserService
from app.auth.service import AuthService
from flask import request
from flask_restful import Resource

arguments = {
	'POST': {
		'required' : ['email' , 'password']
		}
	}

user_service = UserService()
auth_service = AuthService()

class BasicAuth(Resource):

	def post(self):
		args = request.data
		marshalled = utils.marshal_request(args, arguments['POST'])

		marshal_error = utils.make_marshal_error(marshalled)
		if marshal_error:
			return marshal_error

		args = marshalled[0]
		user = user_service.find_by_email(args['email'])
		if not user:
			message = 'User %s not found' % args['email']
			source = 'email'
			return utils.make_error(errors.InvalidParameterError(message, source))

		if not user_service.password_matches(user, args['password']):
			message = 'Password is incorrect'
			source = 'password'
			return utils.make_error(errors.InvalidParameterError(message, source))

		token = auth_service.make_token(user)
		return utils.make_response(data = { 'token': token })
