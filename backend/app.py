import configparser
import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from backend.services.schema_validations.schema_validator import validate, ValidationResultEnum

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://user:password@localhost/db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

db = SQLAlchemy(app)


def create_app_context():
    with app.app_context():
        db.create_all()


class RunResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool = db.Column(db.String(16), nullable=False, index=True)
    project = db.Column(db.String(32), nullable=False, index=True)
    time = db.Column(db.DateTime, nullable=False)
    data = db.Column(db.JSON)

    def __repr__(self):
        return f"<RunResult {self.id} {self.tool} {self.project} {self.time} {self.data}>"


@app.route("/get_all_data", methods=["GET"])
def get_data_per_tool():
    data = RunResult.query.all()
    return jsonify([{"tool": d.tool, "project": d.project, "time": d.time, "data": d.data} for d in data])


@app.route("/run_result", methods=["POST"])
def add_data():
    data = request.json

    validation_result = validate(data["tool"], data["data"])
    if validation_result.result != ValidationResultEnum.SUCCESS:
        return {"error": validation_result.validation_errors}, 400

    project = data["data"].pop("project")

    new_data = RunResult(
        tool=data["tool"],
        project=project,
        time=datetime.fromisoformat(data["time"].replace("Z", "+00:00")),
        data=data["data"]
    )
    db.session.add(new_data)
    db.session.commit()
    return {"id": new_data.id}, 201


if __name__ == "__main__":
    create_app_context()
    app.run(debug=True)
