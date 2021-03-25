import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object(Config)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'
db = SQLAlchemy(app)

# app.config['SECRET_KEY'] = os.urandom(24)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'



from app import views
