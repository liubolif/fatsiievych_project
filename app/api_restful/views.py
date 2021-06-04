# -*- coding: utf-8 -*-
from functools import wraps
import requests
from flask import request, jsonify, make_response
from app.api_restful import api_restful_bp
from app.task.models import Task, Category
from app.profile.models import User
from app import db, bcrypt
# import flask.scaffold
# flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

api = Api(api_restful_bp)

task_create_args = reqparse.RequestParser()
task_create_args.add_argument('title', type=str, help='"title" field is required', required=True)
task_create_args.add_argument('description', type=str, help='"description" field is required', required=True)
task_create_args.add_argument('priority', type=str, help='"priority" field is required', required=True)
task_create_args.add_argument('category_id', type=int, help='"category id" field is required', required=True)

task_update_args = reqparse.RequestParser()
task_update_args.add_argument('title', type=str, help='"title" field is required', required=True)
task_update_args.add_argument('description', type=str, help='"description" field is required', required=True)
task_update_args.add_argument('priority', type=str, help='"priority" field is required', required=True)
task_update_args.add_argument('is_done', type=bool, help='"is done" field is required', required=True)
task_update_args.add_argument('category_id', type=int, help='"category id" field is required', required=True)

resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'created': fields.String,
    'priority': fields.String,
    'category': fields.String,
    'is_done': fields.Boolean
}


class AllTasks(Resource):
    def get(self):
        tasks = Task.query.all()
        tasks_list = {}
        for t in tasks:
            tasks_list[t.id] = {"id": t.id, "title": t.title, "description": t.description, "created": str(t.created),
                                "category": t.categor.name, "is_done": t.is_done}
        return tasks_list

    @marshal_with(resource_fields)
    def post(self):
        args = task_create_args.parse_args()
        try:
            #category_obj = Category.query.get_or_404(args['category_id'])
            task = Task(title=args['title'], description=args['description'], priority=args['priority'],
                        category_id=args['category_id'])
            # for e in data['employee']:
            #    task.for_empl.append(Employee.query.get_or_404(e))
            db.session.add(task)
            db.session.commit()
            return task, 201
        except:
            db.session.rollback()
            abort(400, message="Error occurred during writing the data!")


class OneTask(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        task = Task.query.filter_by(id=id).first()
        if not task:
            abort(404, message="Task not found!")

        return task

    # @marshal_with(resource_fields)
    def delete(self, id):
        task = Task.query.filter_by(id=id).first()

        if not task:
            abort(404, message="Task not found!")

        db.session.delete(task)
        db.session.commit()

        # response = requests.get('http://127.0.0.1:8080/api/tasks').json()
        return 'Task deleted', 204

    @marshal_with(resource_fields)
    def put(self, id):
        task = Task.query.filter_by(id=id).first()

        if not task:
            abort(404, message="Task not found!")

        args = task_update_args.parse_args()

        task.title = args['title']
        task.description = args['description']
        task.priority = args['priority']
        task.category_id = args['category_id']
        task.is_done = args['is_done']

        try:
            db.session.commit()
            return task, 201
        except:
            db.session.rollback()
            abort(400, message="Error occurred during writing the data!")


api.add_resource(AllTasks, '/tasks')
api.add_resource(OneTask, '/tasks', '/tasks/<int:id>')
