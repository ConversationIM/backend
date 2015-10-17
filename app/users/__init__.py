from app.common import utils, errors, exceptions
from app.users.service import UserService
from flask import request
from flask_restful import Resource

arguments = {
    'POST': {
        'required': ['email', 'password', 'confirmedPassword', 'firstName', 'lastName']
    }
}

user_service = UserService()

class User(Resource):

    def post(self):
        args = request.data
        marshalled = utils.marshal_request(args, arguments['POST'])

        marshal_error = utils.make_marshal_error(marshalled)
        if marshal_error:
            return marshal_error

        args = marshalled[0]
        args['active'] = True
        if args.get('password') != args.get('confirmedPassword'):
            message = "Confirmed password did not match password"
            source = "confirmedPassword"
            return utils.make_error(errors.InvalidParameterError(message, [source]))

        existing_user = user_service.find_by_email(args.get('email'))
        if existing_user:
            message = "The user " + args.get('email') + " already exists"
            source = "email"
            return utils.make_error(errors.InvalidParameterError(message, [source]))

        user = None
        try:
            user = user_service.create(args)
        except exceptions.ValidationException, e:
            return utils.make_validation_error(e)
        
        return utils.make_response(data=user.to_dict())
