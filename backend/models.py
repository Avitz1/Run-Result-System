from . import db


class RunResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool = db.Column(db.String(16), nullable=False, index=True)
    project = db.Column(db.String(32), nullable=False, index=True)
    time = db.Column(db.DateTime, nullable=False)
    data = db.Column(db.JSON)

    def __repr__(self):
        return (
            f"<RunResult {self.id} {self.tool} {self.project} {self.time} {self.data}>"
        )


class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False, index=True)
    schema = db.Column(db.JSON)

    def __repr__(self):
        return f"<Tool {self.id} {self.name} {self.schema}>"
