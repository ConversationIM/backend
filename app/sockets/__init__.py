from json import loads
from flask import request
from flask_socketio import emit, join_room, leave_room, disconnect
from app.auth.decorators import authenticated_event
    
class SocketSetupService(object):
    
    sockets = {}
 
    @staticmethod
    def setup_handlers(socketio):
        
        @socketio.on('initialize', namespace="/global")
        @authenticated_event
        def global_init(raw_data, data=None, user=None, error=None):
            if error:
                emit('error', error)
                return disconnect()
            if not user:
                emit('error', "Authentication is required to initialize this namespace")
                return disconnect()
            
            sockets[user.email] = { 'global': request.sid }
            print(sockets)
            
        @socketio.on('initialize', namespace="/conversation")
        @authenticated_event
        def conversation_init(raw_data, data=None, user=None, error=None):
            if error:
                emit('error', error)
                return disconnect()
            if not user:
                emit('error', "Authentication is required to initialize this namespace")
                return disconnect()
            if user.email not in sockets:
                emit('error', "The global namespace must be initialized before this namespace")
                return disconnect()
            
            sockets[user.email]['conversation'] = request.sid
        
#         @socketio.on('join', namespace="/mvp")
#         @authenticated_event
#         def handle_join(raw_data, data = None, user = None, error = None):
#             if error:
#                 return emit('error', error)
#             
#             requested_room = data.get('room')
#             if requested_room != 'default':
#                 # we will only restrict the room for the MVP
#                 error = "Sorry, but only the 'default' room is available"
#                 return emit('error', error)
#             
#             join_room(requested_room)
#             emit('joined', {'room': requested_room})
#  
#         @socketio.on('updated', namespace="/mvp")
#         def handle_update(json):
#             data = loads(json)
#             data = {"message": data.get('message'), "sender": data.get("sender")}
#             emit('updated', data, room=data.get("room"), broadcast=True)
#             
#         @socketio.on('sent', namespace="/mvp")
#         def handle_send(json):
#             #violating DRY in order to get the MVP done faster
#             data = loads(json)
#             data = {"message": data.get('message'), "sender": data.get("sender")}
#             emit('sent', data, room=data.get("room"), broadcast=True)