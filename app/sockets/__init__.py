from json import loads
from flask.ext.socketio import emit, join_room, leave_room
from app.auth.decorators import authenticated_event
    
class SocketSetupService(object):
    """
    Handles all operations related to socketio handler setup
    """
 
    @staticmethod
    def setup_handlers(socketio):
        
        @socketio.on('join', namespace="/mvp")
        @authenticated_event
        def handle_join(raw_data, data = None, user = None, error = None):
            if error:
                return emit('error', error)
            
            requested_room = data.get('room')
            if requested_room != 'default':
                # we will only restrict the room for the MVP
                error = "Sorry, but only the 'default' room is available"
                return emit('error', error)
            
            join_room(requested_room)
            emit('joined', {'room': requested_room})
 
        @socketio.on('sent')
        def handle_send(json):
            data = loads(json)
            emit('sent', data, broadcast=True)