from app import api
from app.users.models import User as model
from flask_restful import Resource, reqparse
from flask_user import UserManager
from flask_user.db_adapters import SQLAlchemyAdapter

post_parser = reqparse.RequestParser()
post_parser.add_argument('email', required=True, type=str)

def init(app, api, database):
    user_manager = UserManager(SQLAlchemyAdapter(database,  model), app)

    class User(Resource):

        def post(self):
            args = post_parser.parse_args()
            return args

    api.add_resource(User, '/users')
