from app import db
from datetime import datetime

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self, tasks=False):
        goal = dict(
            id=self.goal_id,
            title=self.title)
        if tasks:
            goal["tasks"] = [task.to_dict() for task in self.tasks]
        return goal

    @classmethod
    def from_dict(cls,req_body):
        return cls(
            title=req_body['title']
    )