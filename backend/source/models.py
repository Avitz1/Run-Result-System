import json

from backend.source import db


class RunResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool = db.Column(db.String(16), nullable=False, index=True)
    project = db.Column(db.String(32), index=True)
    time = db.Column(db.DateTime, nullable=False)
    data = db.Column(db.JSON)

    def __repr__(self):
        return (
            f"<RunResult {self.id} {self.tool} {self.project} {self.time} {self.data}>"
        )

    def to_dict(self):
        return {
            'id': self.id,
            'tool': self.tool,
            'project': self.project,
            'time': self.time.strftime('%Y-%m-%d %H:%M:%S'),
            'data': self.data
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False, index=True, unique=True)
    schema = db.Column(db.JSON)

    def __repr__(self):
        return f"<Tool {self.id} {self.name} {self.schema}>"
