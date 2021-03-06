from datetime import datetime
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Task('{self.id}', '{self.title}', '{self.description}')"
