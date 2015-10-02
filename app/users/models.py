from app import database as db
from app.common.mixins import general, models

class User(db.Model, general.Serializable):
    __tablename__ = 'users'
    __public__ = ['id', 'email', 'first_name', 'last_name', 'active']

    id = db.Column('ID', db.Integer, primary_key=True)

    email = db.Column('Email', db.Unicode(255), nullable=False, unique=True)
    password = db.Column('Password', db.String(255), nullable=False)
    first_name = db.Column('First_Name', db.Unicode(100), nullable=False)
    last_name = db.Column('Last_Name', db.Unicode(150), nullable=False)
    active = db.Column('Is_Active', db.Boolean(), nullable=False, server_default='0')

class UserDao(models.BaseDao):

    def __init__(self):
        super(UserDao, self).__init__(User)

    def find_by_email(self, email):
        return self.get_query_builder().filter_by(email=email).first()
