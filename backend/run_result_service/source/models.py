import json
from datetime import datetime

from . import db


class RunResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool = db.Column(db.String(16), nullable=False, index=True)
    project = db.Column(db.String(32), index=True)
    user = db.Column(db.String(32), index=True)
    time = db.Column(db.DateTime, nullable=False)
    data = db.Column(db.JSON)

    def __repr__(self):
        return f"<RunResult {self.id} {self.tool} {self.project} {self.user} {self.time} {self.data}>"

    def to_dict(self):
        return {
            "id": self.id,
            "tool": self.tool,
            "project": self.project,
            "user": self.user,
            "time": self.time.strftime("%Y-%m-%d %H:%M:%S"),
            "data": self.data,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def from_dict(data):
        return RunResult(
            tool=data["tool"],
            project=data["project"],
            user=data["user"],
            time=datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S"),
            data=data["data"],
        )


class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False, index=True, unique=True)
    schema = db.Column(db.JSON)

    def __repr__(self):
        return f"<Tool {self.id} {self.name} {self.schema}>"
