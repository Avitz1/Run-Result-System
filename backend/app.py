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
    data = db.Column(db.String(100), nullable=False)
    time = db.Column(db.Date)


@app.route("/get_all_data", methods=["GET"])
def get_data_per_tool():
    data = run_result.query.all()

    return jsonify(
        [{"id": x.id, "tool": x.tool, "data": x.data, "time": x.time} for x in data]
    )


@app.route("/add_data", methods=["POST"])
def add_data():
    data = request.json
    new_data = run_result(tool=data["tool"], data=data["data"], time=datetime.now())
    db.session.add(new_data)
    db.session.commit()
    return {"id": new_data.id}


if __name__ == "__main__":
    app.run(debug=True)
