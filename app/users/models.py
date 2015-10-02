import re
from app import database as db
from app.common import exceptions
from app.common.mixins import general, models
from sqlalchemy.orm import validates

_email_regex = r"[^@]+@[^@]+\.[^@]+"

class User(db.Model, general.Serializable):
    __tablename__ = 'users'
    __public__ = ['id', 'email', 'first_name', 'last_name', 'active']

    id = db.Column('ID', db.Integer, primary_key=True)

    email = db.Column('Email', db.Unicode(255), nullable=False, unique=True)
    password = db.Column('Password', db.String(255), nullable=False)
    first_name = db.Column('First_Name', db.Unicode(100), nullable=False)
    last_name = db.Column('Last_Name', db.Unicode(150), nullable=False)
    active = db.Column('Is_Active', db.Boolean(), nullable=False, server_default='0')

    @validates('email')
    def validate_email(self, key, value):
        value = value.strip()
        if not re.match(_email_regex, value):
            raise exceptions.ValidationException("Email format invalid", key)
        if len(value) > 255:
            raise exceptions.ValidationException("Email cannot be longer than 255 characters", key)
        return value
    
    @validates('first_name')
    def validate_first_name(self, key, value):
        value = value.strip()
        if len(value) > 100 or len(value) == 0:
            raise exceptions.ValidationException("First name must be between 1 and 100 characters", key)
        return value
    
    @validates('last_name')
    def validate_first_name(self, key, value):
        value = value.strip()
        if len(value) > 150 or len(value) == 0:
            raise exceptions.ValidationException('Last name must be between 1 and 150 characters', key)
    

class UserDao(models.BaseDao):

    def __init__(self):
        super(UserDao, self).__init__(User)

    def find_by_email(self, email):
        return self.get_query_builder().filter_by(email=email).first()
