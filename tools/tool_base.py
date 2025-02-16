from abc import ABC, abstractmethod
import json
from jsonschema import validate as validate_schema, ValidationError


class Tool(ABC):
    def __init__(self, schema):
        self.schema = schema

    def validate_result(self, result):
        try:
            validate_schema(instance=result, schema=self.schema)
        except ValidationError as e:
            raise ValueError(f"Invalid result data: {e.message}")
