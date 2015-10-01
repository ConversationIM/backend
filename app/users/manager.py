import bcrypt

from app.common import language
from app.users.models import UserDao

class UserManager(object):

    def __init__(self):
        self.dao = UserDao()

    def _hash_password(self, password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def create(self, parameters):
        parameters = language.pythonize_dict(parameters)
        parameters['password'] = self._hash_password(parameters['password'])
        del parameters['confirmed_password']

        return self.dao.create(**parameters)

    def find_by_email(self, email):
        return self.dao.find_by_email(email)

    def password_matches(self, user, password):
        return bcrypt.hashpw(password, user['password']) == user['password']
