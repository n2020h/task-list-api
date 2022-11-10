from app import db
from datetime import datetime
#from app.models.task import Task
#from sqlalchemy.orm import joinedload

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")
    #tasks = db.relationship("Task", back_populates="goal", nullable = True) #should I change to this?
    #def __repr_(self):
        #"<Task(URL='%s', title = '%', description = '%', completed_at ='%')>" % (self.url, self.title, self.description, self.completed_at)

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