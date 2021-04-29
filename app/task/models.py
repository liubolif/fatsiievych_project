from app import db
import enum
from datetime import datetime


class EnumPriority(enum.Enum):
    low = 1
    medium = 2
    high = 3


many_to_many = db.Table('Task_Employee',
                        db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
                        db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'))
                        )


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    # priority = db.Column(db.Enum('low', 'medium', 'high'), nullable=False)
    priority = db.Column(db.Enum(EnumPriority), default='low')
    is_done = db.Column(db.Boolean, default=False)

    category_id = db.Column(db.Integer(), db.ForeignKey('category.id'))

    def __repr__(self):
        return f"Task('{self.id}', '{self.title}', '{self.description}', '{self.created}', '{self.priority}'," \
               f" '{self.is_done}', category_id='{self.category_id}')\n"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    tasks = db.relationship('Task', backref='categor', lazy='dynamic')

    def __repr__(self):
        return f"Category('{self.id}', '{self.name}')\n"


class Employee(db.Model):  # many to many з Tasks
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    count_of_compltd_task = db.Column(db.Integer, nullable=False, default=0)

    tasks_todo = db.relationship('Task', secondary=many_to_many, backref=db.backref('for_empl'))

    def __repr__(self):
        return f"Employee('{self.id}', '{self.name}', '{self.count_of_compltd_task}')\n"