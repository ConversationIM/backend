import logging
import traceback

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

from app.users import User
api.add_resource(User, '/users')

def initialize():
    _initialize_logging()

    socketio.run(app)

def _initialize_logging():
    # TODO: add more specific configuration parameters
    logging.basicConfig(level=config.LOGGING_LEVEL)
