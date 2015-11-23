from json import loads
from flask import request, current_app
from flask_socketio import emit, join_room, leave_room
from app.auth.decorators import authenticated_event
from app.common.errors import InvalidOperationException
from test.test_socket import _socket

class SocketService(object):
    
    _sockets = {}
    
    @staticmethod
    def _enter_room(socket_id, conversation_id, participant):
        socketio = flask.current_app.extensions['socketio']
        socketio.server.enter_room(socket_id, conversation_id, namespace=flask.request.namespace)
    
    @staticmethod
    def add_global_identifier(email, socket_identifier):
        _sockets[email] = { 'global': socket_identifier }
    
    @staticmethod
    def add_conversation_identifier(email, socket_identifier):
        if email not in sockets:
            raise InvalidOperationException("The global namespace must be initialized before this namespace")
        _sockets[email]['conversation'] = socket_identifier
        
    @staticmethod
    def create_conversation(conversation_id, creator, participants):
        result = [creator]
        SocketService._enter_room(flask.request.sid, conversation_id, creator)
        
        for participant in participants:
            if participant in _sockets:
                global_socket_id = _sockets[participant]['global']
                conversation_socket_id = _sockets[participant]['conversation']
                
                SocketService._enter_room(conversation_socket_id, conversation_id, participant)
                emit('added', namespace='global', room=global_socket_id)
                
                result.append(participant)
                
        return result
    
class SocketSetupService(object):
 
    @staticmethod
    def setup_handlers(socketio):
        
        @socketio.on('initialize', namespace="/global")
        @authenticated_event
        def global_init(raw_data, data=None, user=None, error=None):
            if not user:
                emit('error', "Authentication is required to initialize this namespace")
            if error:
                emit('error', error)
                
            SocketService.add_global_identifier(user.email, request.sid)
            
        @socketio.on('initialize', namespace="/conversation")
        @authenticated_event
        def conversation_init(raw_data, data=None, user=None, error=None):
            if not user:
                emit('error', "Authentication is required to initialize this namespace")
            if error:
                emit('error', error)
            try:
                SocketService.add_conversation_identifier(user.email, request.sid)
            except InvalidOperationException, e:
                emit('error', e.message)
        
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