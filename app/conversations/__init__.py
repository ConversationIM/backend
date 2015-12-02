import random, string
from app.common import utils, errors
from app.auth.decorators import authenticated_request
from app.sockets.service import SocketService
from flask import request
from flask_restful import Resource

arguments = {
    'POST': {
        'required' : ['participants']
    } ,
    'PUT': {'allowed' : ['add', 'remove']
    }
}

class Conversation(Resource):

    @authenticated_request
    def post(self, user=None):
        """
        Creates a new conversation
        """
        
        args = request.data
        marshalled = utils.marshal_request(args, arguments['POST'])

        marshal_error = utils.make_marshal_error(marshalled)
        if marshal_error:
            return marshal_error

        args = marshalled[0]
        participants = args['participants']
        conversation_id = ''.join(random.choice(string.lowercase) for i in range(25))
        
        result = SocketService.create_conversation(conversation_id, user['email'], participants)
        return utils.make_response(data = { 'conversationId': conversation_id, 'participants': result })

    @authenticated_request
    def put(self, id=None, user=None):
        """
        Removes the user from the conversation
        """
        args = request.data
        marshalled = utils.marshal_request(args, arguments['PUT'])

        marshal_error = utils.make_marshal_error(marshalled)
        if marshal_error:
            return marshal_error

        SocketService.leave_conversation(id, user['email'])
