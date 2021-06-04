from flask import Blueprint
from flask_admin import Admin

user_bp = Blueprint('user_bp_in', __name__, static_folder='static', static_url_path='/static/user_bp_in',
                    template_folder="templates/profile")


from .views import MyAdminIndexView

#admin = Admin(index_view=views.MyAdminIndexView())

def create_module(app, **kwargs):
    from .views import CustomView, UserModelView
    from .. import db
    from .models import User
    admin = Admin(index_view=views.MyAdminIndexView())
    admin.init_app(app)
    admin.add_view(CustomView(name='Custom'))
    admin.add_view(UserModelView(User, db.session))

from . import views
