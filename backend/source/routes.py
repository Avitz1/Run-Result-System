from flask import Blueprint, request, jsonify
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from backend.source.models import RunResult, Tool
from backend.source import db
from backend.source.services.schema_validations.schema_validator import validate, ValidationResultEnum
from backend.source.services.tools_cache import get_cached_tools

main = Blueprint("main", __name__)


@main.route("/get_tools", methods=["GET"])
def get_tools():
    tools = get_cached_tools()
    return jsonify([{"name": t.name, "schema": t.schema} for t in tools])


@main.route("/admin/add_tool", methods=["POST"])
def add_tool():
    data = request.json
    new_tool = Tool(name=data["name"], schema=data["schema"])
    db.session.add(new_tool)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Tool with this name already exists."}), 400

    return {"id": new_tool.id}, 201


@main.route("/get_filtered_data", methods=["GET"])
def get_filtered_data():

    last_id = request.args.get("last_id", None, type=int)
    per_page = request.args.get(
        "per_page", 1000, type=int
    )
    start_date = request.args.get("start_date", None)
    end_date = request.args.get("end_date", None)
    tool = request.args.get("tool", None)
    username = request.args.get("username", None)
    project = request.args.get("project", None)

    query = RunResult.query

    if (start_date and not end_date) or (not start_date and end_date):
        return jsonify({"error": "Both start_date and end_date must be provided."}), 400

    if last_id:
        query = query.filter(RunResult.id > last_id)
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(RunResult.time.between(start_date, end_date))
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    if username:
        query = query.filter_by(username=username)
    if tool:
        query = query.filter_by(tool=tool)
    if project:
        query = query.filter_by(project=project)

    query = query.order_by(RunResult.id)

    query = query.limit(per_page)
    data = query.all()

    return jsonify(
        {
            "data": [
                {
                    "id": d.id,
                    "tool": d.tool,
                    "project": d.project,
                    "time": d.time.isoformat(),
                    "data": d.data,
                }
                for d in data
            ],
            "last_id": data[-1].id if data else None,
        }
    )


@main.route("/run_result", methods=["POST"])
def add_data():
    data = request.json

    validation_result = validate(data["tool"], data["data"])
    if validation_result.result != ValidationResultEnum.SUCCESS:
        return {"error": validation_result.validation_errors}, 400

    if data["data"].get("project"):
        project = data["data"].pop("project")
    else:
        project = None

    new_data = RunResult(
        tool=data["tool"],
        project=project,
        time=datetime.fromisoformat(data["time"].replace("Z", "+00:00")),
        data=data["data"],
    )
    db.session.add(new_data)
    db.session.commit()
    return {"id": new_data.id}, 201
