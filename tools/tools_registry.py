from tools.tool_base import Tool


class ToolRegistry:
    _tools = {}

    @classmethod
    def register_tool(cls, tool_name, tool):
        cls._tools[tool_name] = tool

    @classmethod
    def get_tool(cls, tool_name):
        if tool_name in cls._tools:
            return cls._tools[tool_name]
        else:
            return None


ToolRegistry.register_tool('innovus', Tool({
    "type": "object",
    "properties": {
        "user": {"type": "string"},
        "project": {"type": "string"},
        "tag": {"type": "string"},
        "t_deviate": {"type": "number"},
        "path_type": {"type": "string"}
    },
    "required": ["user", "project", "tag", "t_deviate", "path_type"]
}))

ToolRegistry.register_tool('prime', Tool({
    "type": "object",
    "properties": {
        "user": {"type": "string"},
        "project": {"type": "string"},
        "tag": {"type": "string"},
        "aberrant_cells": {"type": "array", "items": {"type": "string"}},
        "avg_aberration": {"type": "number"},
        "edge_focus": {"type": "array", "items": {"type": "integer"}}
    },
    "required": ["user", "project", "tag", "aberrant_cells", "avg_aberration", "edge_focus"]
}))
