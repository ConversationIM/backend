from app import api_v1
from app.users.manager import Manager
from flask_restful import Resource, reqparse

user_manager = Manager().get_instance()

post_parser = reqparse.RequestParser()
post_parser.add_argument('email', required=True, type=str)

class User(Resource):
    def post(self):
        args = post_parser.parse_args()
        print(args)

api_v1.add_resource(User, '/user')
