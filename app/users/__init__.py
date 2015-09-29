from flask_restful import Resource, reqparse

post_parser = reqparse.RequestParser()
post_parser.add_argument('email', required=True, type=str)

class User(Resource):
    def post(self):
        args = post_parser.parse_args()
        print(args)
