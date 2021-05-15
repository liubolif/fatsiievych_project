from datetime import datetime
from app import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime


# This callback is used to reload the user object from the user ID stored in the session.
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    def __init__(self, username, email, password, admin):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.admin = admin

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    about_me = db.Column(db.Text, nullable=True)
    image_file = db.Column(db.String(20), nullable=False, server_default='default.png')
    last_time_seen = db.Column(db.DateTime, default=datetime.utcnow)
    admin = db.Column(db.Boolean, default=False)

    def is_admin(self):
        return self.admin

    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}', '{self.password}', '{self.last_time_seen}')\n"
