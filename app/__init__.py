import logging
import traceback

from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask.ext.socketio import SocketIO

from config import ConfigFactory
from common import errors

config = ConfigFactory.build_config()

app = Flask(__name__)
app.config.from_object(config)

api = Api(app, '/v1')
database = SQLAlchemy(app)
socketio = SocketIO(app)

def initialize():
    _initialize_logging()
    _initialize_resources()
    _initialize_socketio()

    socketio.run(app, host=config.HOST, port=config.PORT)

def _initialize_logging():
    if config.LOG_LOCATION:
        from app.common.errors import ApiError
        from app.common.utils import make_error

        @app.errorhandler(500)
        def internal_server_error(error):
            app.logger.error('Server Error: %s', (error))
            return make_error(ApiError())

        @app.errorhandler(Exception)
        def unhandled_exception(e):
            app.logger.error('Unhandled Exception: %s', (e))
            return make_error(ApiError())

        handler = RotatingFileHandler(config.LOG_LOCATION, maxBytes=10000, backupCount=1)
        handler.setLevel(config.LOGGING_LEVEL)
        app.logger.addHandler(handler)
    else:
        logging.basicConfig(level=config.LOGGING_LEVEL)

def _initialize_resources():
    from app.users import User
    api.add_resource(User, '/users', '/users/<int:id>')
    from app.auth import BasicAuth
    api.add_resource(BasicAuth, '/auth')
    from app.conversations import Conversation
    api.add_resource(Conversation, '/conversation', '/conversation/<string:id>')

def _initialize_socketio():
    from app.sockets.service import SocketSetupService
    SocketSetupService.setup_handlers(socketio)
