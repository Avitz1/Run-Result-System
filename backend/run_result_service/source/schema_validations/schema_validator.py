from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, List

from backend.run_result_service.source.tools_cache import get_cached_tool


class ValidationResultEnum(Enum):
    SUCCESS = "success"
    TOOL_NOT_FOUND = "tool_not_found"
    MISSING_FIELDS = "missing_fields"
    REDUNDANT_FIELDS = "redundant_fields"
    INVALID_TYPES = "invalid_types"


@dataclass
class ValidationResult:
    result: ValidationResultEnum
    validation_errors: Dict[str, List[str]]


def validate_field(field: any, field_type: any) -> bool:
    """
    Validates a single field against its type.
    """
    if isinstance(field_type, list):
        elements_type = eval(field_type[1])
        if elements_type == str:
            return isinstance(field, list) and all(isinstance(item, str) for item in field)
        elif elements_type == int:
            return isinstance(field, list) and all(isinstance(item, int) for item in field)
        elif elements_type == float:
            return isinstance(field, list) and all(isinstance(item, int) or isinstance(item, float) for item in field)
    else:
        return isinstance(field, eval(field_type))


def validate(tool: str, data: Dict[str, Any]) -> ValidationResult:
    """
    Validates the incoming data against the tool's schema.
    """
    tool = get_cached_tool(tool)
    if tool is None:
        return ValidationResult(ValidationResultEnum.TOOL_NOT_FOUND,
                                {ValidationResultEnum.TOOL_NOT_FOUND.value: "try with an existing tool"})
    else:
        schema = tool.schema
        missing_fields = [field for field in schema if field not in data]
        if missing_fields:
            return ValidationResult(ValidationResultEnum.MISSING_FIELDS,
                                    {ValidationResultEnum.MISSING_FIELDS.value: missing_fields})
        redundant_fields = [field for field in data if field not in schema]
        if redundant_fields:
            return ValidationResult(ValidationResultEnum.REDUNDANT_FIELDS,
                                    {ValidationResultEnum.REDUNDANT_FIELDS.value: redundant_fields})
        invalid_types = [f'field \"{field}\" should be {field_type}' for field, field_type in schema.items()
                         if not validate_field(data[field], field_type)]
        if invalid_types:
            return ValidationResult(ValidationResultEnum.INVALID_TYPES,
                                    {ValidationResultEnum.INVALID_TYPES.value: invalid_types})

        return ValidationResult(ValidationResultEnum.SUCCESS, {})
