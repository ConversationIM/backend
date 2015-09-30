import re

from flask_user.db_adapters import SQLAlchemyAdapter
from flask_user import UserManager as BaseManager
from app.users.models import User

class UserManager(BaseManager):

    def __init__(self, app, database):
        database_adapter = SQLAlchemyAdapter(database,  User)
        super(UserManager, self).__init__(database_adapter, app)

    def add_user(self, parameters):
        # TODO: put this in a utilities module
        creation_parameters = {}
        for key, value in parameters.iteritems():
            key = re.sub("([A-Z])", "_\g<1>", key).lower()
            creation_parameters[key] = value

        creation_parameters['password'] = self.hash_password(creation_parameters['password'])
        del creation_parameters['confirmed_password']

        self.db_adapter.add_object(User, **creation_parameters)
        self.db_adapter.commit()
