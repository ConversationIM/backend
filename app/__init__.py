from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask.ext.socketio import SocketIO

from config import ConfigFactory
from example import Example

config = ConfigFactory.build_config()

_app = Flask(__name__)
_app.config.from_object(config)

_app_v1 = Blueprint('v1', __name__)

api = Api(_app_v1)
database = SQLAlchemy(_app)
socketio = SocketIO(_app)

def initialize():
    _initialize_logging()
    _initialize_apis()
    _initialize_blueprints()
    
    socketio.run(_app)

def _initialize_logging():
    import logging
    
    # TODO: add more specific configuration parameters
    logging.basicConfig(level=config.LOGGING_LEVEL)
    
def _initialize_apis():
    # if we had multiple versions of the api to initialize, 
    # we would initialize api_v1, api_v2, etc here
    api.add_resource(Example, '/example')
    
def _initialize_blueprints():
    # if we had multiple versions of the api, we would initialize
    # the blueprint for each here
    _app.register_blueprint(_app_v1, url_prefix='/v1')