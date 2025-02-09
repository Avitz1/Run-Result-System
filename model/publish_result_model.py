from dataclasses import dataclass
from enum import Enum
from http import HTTPStatus


@dataclass
class PublishResultRequest:
    def __init__(self, tool, data, time):
        self.__tool = tool
        self.__data = data
        self.__time = time

    def toJSON(self):
        return {"tool": self.__tool, "data": self.__data, "time": self.__time}


class PublishResultErrorMessagesEnum(Enum):
    TOOL_DOES_NOT_EXIST = "Tool does not exist"
    PROJECT_DOES_NOT_EXIST = "Project does not exist"
    DATA_FIELDS_MISSING = "Data fields missing"
    SCHEMA_VIOALTION = "Schema violation"


@dataclass
class PublishResultResponse:
    def __init__(self, httpStatus: HTTPStatus, error_message: PublishResultErrorMessagesEnum, schema: str = None):
        self.__httpStatus = httpStatus
        self.__error_message = error_message
        self.__schema = schema
