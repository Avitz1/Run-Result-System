from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class run_result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool = db.Column(db.String(16), nullable=False, index=True)
    time = db.Column(db.Date)
    json_data = db.Column(db.JSON)

    def __repr__(self):
        return f"<RunResult {self.id}, {self.tool}, {self.json_data}, {self.time}>"


@app.route("/get_all_data", methods=["GET"])
def get_data_per_tool():
    data = run_result.query.all()
    return jsonify(
        [
            {"id": x.id, "tool": x.tool, "time": x.time, "json_data": x.json_data}
            for x in data
        ]
    )


@app.route("/add_data", methods=["POST"])
def add_data():
    data = request.json
    new_data = run_result(
        tool=data["tool"], time=datetime.now(), json_data=data.get("json_data", {})
    )
    db.session.add(new_data)
    db.session.commit()
    return {"id": new_data.id}, 201


if __name__ == "__main__":
    app.run(debug=True)
