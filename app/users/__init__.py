from app import api
from app.users.models import User as model
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_user import UserManager
from flask_user.db_adapters import SQLAlchemyAdapter

post_parser = reqparse.RequestParser()
post_parser.add_argument('email', required=True, type=str)
post_parser.add_argument('password', required=True, type=str)
post_parser.add_argument('confirmedPassword', required=True, type=str)
post_parser.add_argument('firstName', required=True, type=str)
post_parser.add_argument('lastName', required=True, type=str)

def init(app, api, database):
    user_manager = UserManager(SQLAlchemyAdapter(database,  model), app)

    class User(Resource):

        def post(self):
            args = post_parser.parse_args()

            # TODO: figure out how to properly throw errors
            if (args.password != args.confirmedPassword):
                return jsonify({
                    "error": "This would say that password and confirmedPassword are not equivalent"
                })

            existing_user = user_manager.find_user_by_email(args.email)
            if (existing_user[0] is not None):
                return jsonify({
                    "error": "This would say that a user with that email already exists"
                })

            return jsonify({"result": "ok"})

    api.add_resource(User, '/users')
