from flask import Blueprint, request, jsonify
from datetime import datetime
from .models import RunResult
from . import db
from backend.services.schema_validations.schema_validator import validate, ValidationResultEnum

main = Blueprint('main', __name__)


@main.route("/get_all_data", methods=["GET"])
def get_data_per_tool():
    last_id = request.args.get('last_id', None, type=int)
    per_page = request.args.get('per_page', 1000, type=int)  # Default to 1000 rows per page

    query = RunResult.query.order_by(RunResult.id)
    if last_id:
        query = query.filter(RunResult.id > last_id)

    query = query.limit(per_page)
    data = query.all()

    return jsonify({
        "data": [{"id": d.id, "tool": d.tool, "project": d.project, "time": d.time, "data": d.data} for d in data],
        "last_id": data[-1].id if data else None
    })


@main.route("/run_result", methods=["POST"])
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
