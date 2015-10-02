from app.common import errors
from app.common import utils
from app.users.manager import UserManager
from flask import jsonify
from flask_restful import Resource, reqparse

post_parser = reqparse.RequestParser()
post_parser.add_argument('email', required=True, type=str)
post_parser.add_argument('password', required=True, type=str)
post_parser.add_argument('confirmedPassword', required=True, type=str)
post_parser.add_argument('firstName', required=True, type=str)
post_parser.add_argument('lastName', required=True, type=str)

def init(app, api, database):
    # TODO: figure out a way to resolve circular imports that doesn't involve an init function
    # Then we can stop passing the app to the make_error/make_response functions too

    user_manager = UserManager()

    class User(Resource):

        def post(self):
            args = post_parser.parse_args()
            # TODO: check format of arguments (i.e., is email actually an email? Is the input too long?)
            # TODO: try to reformat request parser's errors instead of letting them go

            if args.password != args.confirmedPassword:
                message = "Confirmed password did not match password"
                source = "confirmedPassword"
                return utils.make_error(errors.InvalidParameterError(message, source))

            existing_user = user_manager.find_by_email(args.email)
            if existing_user:
                message = "The user " + args.email + " already exists"
                source = "email"
                return utils.make_error(errors.InvalidParameterError(message, source))

            user = user_manager.create(args)
            return utils.make_response(data=user.to_dict())

    api.add_resource(User, '/users')
