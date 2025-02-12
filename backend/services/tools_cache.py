from backend import cache
from backend.models import Tool


@cache.cached(timeout=5, key_prefix='all_tools')
def get_cached_tools():
    return Tool.query.all()