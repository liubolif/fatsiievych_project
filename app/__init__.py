import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# app = Flask(__name__)

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'user_bp_in.login'
login_manager.login_message = "Please, sign in to have an access to the account"
login_manager.login_message_category = 'info'
db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    with app.app_context():
        # app.config.from_object(Config)
        if os.environ.get('DATABASE_URL') is None:
            app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///testing.db', SECRET_KEY='supersecretkey')
        else:
            app.config.from_object(Config)

        db.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)

        from . import views
        from .profile import user_bp
        from .contact import contact_bp
        from .task import task_bp
        from .api import api_bp
        from .api_restful import api_restful_bp
        from .swagger_ui import SWAGGERUI_BLUEPRINT, SWAGGER_URL

        app.register_blueprint(user_bp, url_prefix='/usr')
        app.register_blueprint(contact_bp, url_prefix='/cnt')
        app.register_blueprint(task_bp, url_prefix='/tsk')
        app.register_blueprint(api_bp, url_prefix='/api')
        app.register_blueprint(api_restful_bp, url_prefix='/api/v2')
        app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

        from .profile import create_module as admin_create_module
        admin_create_module(app)

    return app
