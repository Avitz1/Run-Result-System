from abc import ABC
from jsonschema import validate as validate_schema, ValidationError


class Tool(ABC):
    def __init__(self, schema):
        self.schema = schema

    def validate_result(self, result):
        try:
            validate_schema(instance=result, schema=self.schema)
        except ValidationError as e:
            raise ValidationError(f"Result does not match schema: {e}")
