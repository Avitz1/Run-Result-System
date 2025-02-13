from dataclasses import dataclass


@dataclass
class PublishResultRequest:
    def __init__(self, tool, data, time):
        self.__tool = tool
        self.__data = data
        self.__time = time

    def to_json(self):
        return {"tool": self.__tool, "data": self.__data, "time": self.__time}
