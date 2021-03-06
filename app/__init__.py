import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config


app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(24)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import views
