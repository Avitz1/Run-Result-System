from backend.source import cache
from backend.source.models import Tool


@cache.cached(timeout=1, key_prefix='all_tools')
def get_cached_tools():
    return Tool.query.all()


@cache.cached(timeout=1, key_prefix='tool_')
def get_cached_tool(tool_name):
    return Tool.query.filter_by(name=tool_name).first()