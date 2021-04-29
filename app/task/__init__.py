from flask import Blueprint

task_bp = Blueprint('task_bp_in', __name__, template_folder="templates/task")

from . import views