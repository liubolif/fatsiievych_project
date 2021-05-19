# -*- coding: utf-8 -*-
from functools import wraps

from flask import request, jsonify, make_response
from app.api import api_bp
from app.task.models import Task, Category
from app.profile.models import User
from app import db, bcrypt

from datetime import datetime, timedelta
import jwt
from flask import current_app as app


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@api_bp.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login required!"'})

    if bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                           app.config['SECRET_KEY'])

        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@api_bp.route('/tasks', methods=['GET'])
@token_required
def tasks_all(current_user):
    tasks = Task.query.all()
    output = []

    for task in tasks:
        task_data = {}
        task_data['id'] = task.id
        task_data['title'] = task.title
        task_data['description'] = task.description
        task_data['created'] = task.created
        task_data['priority'] = str(task.priority.name)  # ????
        task_data['category'] = task.categor.name
        task_data['is_done'] = task.is_done
        employees = ""
        for e in task.for_empl:
            employees = employees + e.name + " "
        employees.strip()
        task_data['employees'] = employees
        output.append(task_data)

    return jsonify({"task": output}), 200


@api_bp.route('/tasks/<int:id>', methods=['GET'])
@token_required
def task_detail(current_user, id):
    task = Task.query.filter_by(id=id).first()

    if not task:
        return jsonify({'message': 'Task not found!'}), 404

    task_data = {}
    task_data['id'] = task.id
    task_data['title'] = task.title
    task_data['description'] = task.description
    task_data['created'] = task.created
    task_data['priority'] = str(task.priority.name)  # ????
    task_data['category'] = task.categor.name
    task_data['is_done'] = task.is_done
    employees = ""
    for e in task.for_empl:
        employees = employees + e.name + " "
    employees.strip()
    task_data['employees'] = employees

    return jsonify(task_data), 200


@api_bp.route('/tasks', methods=["POST"])
@token_required
def task_create(current_user):
    data = request.get_json()

    try:
        # category_obj = Category.query.get_or_404(data['category_id'])
        task = Task(title=data['title'], description=data['description'], priority=data['priority'],
                    category_id=data['category_id'])

        #for e in data['employee']:
        #    task.for_empl.append(Employee.query.get_or_404(e))
        db.session.add(task)
        db.session.commit()

        return jsonify({'message': 'Task successfully created!'}), 201

    except:
        db.session.rollback()
        return jsonify({'message': 'Error occurred during writing the data!'}), 400


@api_bp.route('/tasks/<int:id>', methods=["DELETE"])
@token_required
def task_delete(current_user, id):
    task = Task.query.filter_by(id=id).first()

    if not task:
        return jsonify({'message': 'Task not found!'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted!'}), 200


@api_bp.route('/tasks/<int:id>', methods=["PUT"])
@token_required
def task_update(current_user, id):
    task = Task.query.filter_by(id=id).first()

    if not task:
        return jsonify({'message': 'Task not found!'}), 404

    task.title = request.json['title']
    task.description = request.json['description']
    task.priority = request.json['priority']
    task.category_id = request.json['category_id']
    task.is_done = request.json['is_done']
    db.session.commit()

    return jsonify({"message": "Task successfully updated!"}), 201
