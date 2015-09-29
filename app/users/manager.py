from app import _app as app
from app import database as db
from app.users.models import User
from flask_user import UserManager
from flask_user.db_adapters import SQLAlchemyAdapter

class Manager(object):
    __instance = None

    def __init__(self):
        pass

    def get_instance(self):
        if Manager.__instance is None:
            database_adapter = SQLAlchemyAdapter(database,  User)
            Manager.__instance = UserManager(database_adapter, app)

        return Manager.__instance
