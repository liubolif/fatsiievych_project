from flask import Blueprint

api_restful_bp = Blueprint('api_restful_bp_in', __name__)

from . import views
