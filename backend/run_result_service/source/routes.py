import json

from flask import Blueprint, request, jsonify
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from kafka import KafkaProducer
from .models import RunResult, Tool
from . import db
from .schema_validations.schema_validator import validate, ValidationResultEnum
from .tools_cache import get_cached_tools, get_cached_tool

main = Blueprint("main", __name__)

producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    request_timeout_ms=1000,
    retries=3
)


@main.route("/get_tools", methods=["GET"])
def get_tools():
    tools = get_cached_tools()
    return jsonify([{"name": t.name, "schema": t.schema} for t in tools])


@main.route("/get_tool_schema", methods=["GET"])
def get_tool():
    tool_name = request.args.get("name")
    tool = get_cached_tool(tool_name)
    if not tool:
        return jsonify({"error": "Tool not found."}), 404

    return jsonify({"name": tool.name, "schema": tool.schema})


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
    tool = request.args.get("tool", None)
    user = request.args.get("user", None)
    project = request.args.get("project", None)

    # TODO additional fields

    query = RunResult.query

    if last_id:
        query = query.filter(RunResult.id > last_id)
    if user:
        query = query.filter_by(user=user)
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
                    "user": d.user,
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

    new_data = RunResult(
        tool=data["tool"],
        project=data["project"],
        user=data["user"],
        time=datetime.fromisoformat(data["time"].replace("Z", "+00:00")),
        data=data["data"],
    )

    future = producer.send('run-results', new_data.to_json())
    result = future.get(timeout=3)
    kafka_metadata = {
        'topic': result.topic,
        'partition': result.partition,
        'offset': result.offset,
        'timestamp': result.timestamp
    }

    producer.flush()

    return jsonify({"kafka_metadata": kafka_metadata}), 200
