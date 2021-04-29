from flask import Blueprint

contact_bp = Blueprint('contact_bp_in', __name__, template_folder="templates/contact")

from . import views