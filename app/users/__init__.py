from app.common import utils, errors
from app.users.manager import UserManager
from flask import request
from flask_restful import Resource

arguments = {
    'POST': {
        'required': ['email', 'password', 'confirmedPassword', 'firstName', 'lastName']
    }
}

def init(app, api, database):
    # TODO: figure out a way to resolve circular imports that doesn't involve an init function
    # Then we can stop passing the app to the make_error/make_response functions too
    #
    # TODO: check format of arguments (i.e., is email actually an email? Is the input too long?)
    # Not quite sure how to implement this cleanly

    user_manager = UserManager()

    class User(Resource):

        def post(self):
            args = request.data
            marshalled = utils.marshal_request(args, arguments['POST'])

            marshal_error = utils.make_marshal_error(marshalled)
            if marshal_error:
                return marshal_error

            args = marshalled[0]
            if args.get('password') != args.get('confirmedPassword'):
                message = "Confirmed password did not match password"
                source = "confirmedPassword"
                return utils.make_error(errors.InvalidParameterError(message, [source]))

            existing_user = user_manager.find_by_email(args.get('email'))
            if existing_user:
                message = "The user " + args.get('email') + " already exists"
                source = "email"
                return utils.make_error(errors.InvalidParameterError(message, [source]))

            user = user_manager.create(args)
            return utils.make_response(data=user.to_dict())

    api.add_resource(User, '/users')
