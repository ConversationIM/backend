from json import loads
from flask.ext.socketio import emit
from app.auth.decorators import authenticated_event

class SocketSetupService(object):
    """
    Handles all operations related to socketio handler setup
    """

    @staticmethod
    def setup_handlers(socketio):
        
        @socketio.on('connection')     
        @authenticated_event
        def handle_connection(raw_data, data = None, user = None, error = None):
            if error:
                emit('error', error)
            else:
                print(str(user) + " has connected")

        @socketio.on('updated')
        def handle_update(json):
            data = loads(json)
            emit('updated', data, broadcast=True)

        @socketio.on('sent')
        def handle_send(json):
            data = loads(json)
            emit('sent', data, broadcast=True)