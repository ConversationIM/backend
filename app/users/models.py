from app import database as db
from flask_user import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column('ID', db.Integer, primary_key=True)

    # required for Flask-User
    email = db.Column('Email', db.Unicode(255), nullable=False, unique=True)
    password = db.Column('Password', db.String(255), nullable=False)
    active = db.Column('Is_Active', db.Boolean(), nullable=False, server_default='0')
    confirmed_at = db.Column('Confirmed_At', db.DateTime())
    reset_password_token = db.Column('Reset_Password_Token', db.String(100))

    first_name = db.Column('First_Name', db.Unicode(100), nullable=False)
    last_name = db.Column('Last_Name', db.Unicode(150), nullable=False)
