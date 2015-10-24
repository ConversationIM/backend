from json import loads
from flask.ext.socketio import emit, join_room, leave_room
from app.auth.decorators import authenticated_event
    
class SocketSetupService(object):
    """
    Handles all operations related to socketio handler setup
    Note: this is to be used in its current state for the MVP
    ONLY. The functionality has not been throughly tested enough
    to leave it as-is
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
 
        @socketio.on('updated', namespace="/mvp")
        def handle_update(json):
            data = loads(json)
            data = {"message": data.get('message'), "sender": data.get("sender")}
            emit('updated', data, room=data.get("room"), broadcast=True)
            
        @socketio.on('sent', namespace="/mvp")
        def handle_send(json):
            #violating DRY in order to get the MVP done faster
            data = loads(json)
            data = {"message": data.get('message'), "sender": data.get("sender")}
            emit('sent', data, room=data.get("room"), broadcast=True)