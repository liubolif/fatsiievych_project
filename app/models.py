from datetime import datetime
from app import db
import enum
from datetime import datetime


class EnumPriority(enum.Enum):
    low = 1
    medium = 2
    high = 3


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    # priority = db.Column(db.Enum('low', 'medium', 'high'), nullable=False)
    priority = db.Column(db.Enum(EnumPriority), default='low')
    is_done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Task('{self.id}', '{self.title}', '{self.description}', '{self.created}', '{self.priority}'," \
               f" '{self.is_done}')"
