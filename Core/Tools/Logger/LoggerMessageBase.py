import typing
from enum import Enum


class LoggerMessageTypeEnum(Enum):
    STARTUP = "STARTUP"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    EXEC_DETAILS = "EXEC"
    INTEGRATION_EVENT = "INTEGRATION_EVENT"


class LoggerMessageBase:
    def __init__(self,
                 mtype: LoggerMessageTypeEnum = None,
                 name: typing.AnyStr = None,
                 code: int = None,
                 description: typing.AnyStr = None,
                 extra_data: typing.Union[typing.AnyStr, typing.Dict] = None):
        self.type = mtype
        self.name = name
        self.code = code
        self.description = description
        self.extra_data = extra_data

    def to_dict(self):
        details = {
            "details": {
                "type": self.type.value,
                "name": self.name,
                "code": self.code,
                "description": self.description
            }
        }
        try:
            if self.extra_data:
                details["details"].update(self.extra_data)
        except Exception as e:
            details["details"].update({"error": f"Failed to generate log {str(e)}"})

        return details
