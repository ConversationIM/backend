import types
from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask.ext.socketio import SocketIO

from config import ConfigFactory
from decorators import route

config = ConfigFactory.build_config()

_app = Flask(__name__)
_app.config.from_object(config)

_app_v1 = Blueprint('v1', __name__)

api_v1 = Api(_app_v1)
api_v1.route = types.MethodType(route, api_v1)

database = SQLAlchemy(_app)
socketio = SocketIO(_app)

def initialize():
    _initialize_logging()
    _initialize_apis()

    socketio.run(_app)

def _initialize_logging():
    import logging

    # TODO: add more specific configuration parameters
    logging.basicConfig(level=config.LOGGING_LEVEL)

def _initialize_apis():
    _app.register_blueprint(_app_v1, url_prefix='/v1')
