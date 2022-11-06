from app import db
from datetime import datetime

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
