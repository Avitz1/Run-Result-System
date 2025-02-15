from dataclasses import dataclass


@dataclass
class PublishResultRequest:
    def __init__(self, tool, project, user, data, time):
        self.__tool = tool
        self.__project = project
        self.__user = user
        self.__data = data
        self.__time = time

    def to_json(self):
        return {
            "tool": self.__tool,
            "project": self.__project,
            "user": self.__user,
            "data": self.__data,
            "time": self.__time,
        }
