import bcrypt

from app.common import utils
from app.users.models import UserDao

class UserService(object):
    """
    Handles operations related to the management of User
    instances
    """

    def __init__(self):
        self.dao = UserDao()

    def _hash_password(self, password):
        """
        Hashes the provided password using bcrypt
        :password the password to hash
        """

        return bcrypt.hashpw(password, bcrypt.gensalt())

    def create(self, parameters):
        """
        Creates a user with the provided parameters
        :parameters the parameters to use to create the user, which
        must be declared in the User model
        """

        parameters = utils.pythonize_dict(parameters)
        parameters['password'] = self._hash_password(parameters['password'])
        del parameters['confirmed_password']

        return self.dao.create(**parameters)

    def find_by_id(self, id):
        """
        Finds a user by the provided id by invoking the User DAO
        :id the id to query with
        """

        return self.dao.find_by_id(id)

    def find_by_email(self, email):
        """
        Finds a user by the provided email by invoking the User DAO
        :email the email address to query with
        """

        return self.dao.find_by_email(email)
        
    def password_matches(self, user, password):
        """
        Checks to see if the provided user has the provided password
        :user a user instance
        :password a password to check against
        """

        existing_hash = utils.byteify(user.password)
        return bcrypt.hashpw(password, existing_hash) == existing_hash
