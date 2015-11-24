from json import loads
from flask import request, current_app
from flask_socketio import emit, join_room, leave_room
from app.auth.decorators import authenticated_event
from app.common.exceptions import InvalidOperationException
from test.test_socket import _socket

class SocketService(object):
    
    _sockets = {}
    
    @staticmethod
    def _enter_conversation(socket_id, conversation_id, participant):
        socketio = current_app.extensions['socketio']
        socketio.server.enter_room(socket_id, conversation_id, namespace='/conversation')
        
    @staticmethod
    def _get_conversations(socket_id, participant):
        socketio = current_app.extensions['socketio']
        socketio.server.rooms(socket_id, namespace='/conversation')
    
    @staticmethod
    def add_global_identifier(email, socket_identifier):
        SocketService._sockets[email] = { 'global': socket_identifier }
    
    @staticmethod
    def add_conversation_identifier(email, socket_identifier):
        if email not in SocketService._sockets:
            raise InvalidOperationException("The global namespace must be initialized before this namespace")
        SocketService._sockets[email]['conversation'] = socket_identifier
        
    @staticmethod
    def create_conversation(conversation_id, creator, participants):
        result = []
        SocketService._enter_conversation(SocketService._sockets[creator]['conversation'], conversation_id, creator)
        
        for participant in participants:
            if participant in SocketService._sockets:
                global_socket_id = SocketService._sockets[participant]['global']
                conversation_socket_id = SocketService._sockets[participant]['conversation']
                
                request.namespace = '/global'
                request.sid = global_socket_id
                SocketService._enter_conversation(conversation_socket_id, conversation_id, participant)
                emit('added', {'conversationId': conversation_id, 'creator': creator})
                
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
                
            SocketService.add_global_identifier(user['email'], request.sid)
            
        @socketio.on('initialize', namespace="/conversation")
        @authenticated_event
        def conversation_init(raw_data, data=None, user=None, error=None):
            if not user:
                emit('error', "Authentication is required to initialize this namespace")
            if error:
                emit('error', error)
            try:
                SocketService.add_conversation_identifier(user['email'], request.sid)
            except InvalidOperationException, e:
                emit('error', e.message)
        
  
        @socketio.on('updated', namespace="/conversation")
        def conversation_update(json):
            if type(json) is not dict:
                data = loads(json)
            
            emit('updated', data, room=data.get('conversationId'))
             
        @socketio.on('sent', namespace="/conversation")
        def conversation_send(json):
            if type(json) is not dict:
                data = loads(json)

            emit('sent', data, room=data.get("conversationId"))