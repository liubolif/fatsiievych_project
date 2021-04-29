from flask import Blueprint

user_bp = Blueprint('user_bp_in', __name__, static_folder='static', static_url_path='/static/user_bp_in',
                    template_folder="templates/profile")

from . import views