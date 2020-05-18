import json
import os
import typing
from datetime import datetime

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageTypeEnum, LoggerMessageBase

RabbitMessageType = typing.Union[typing.AnyStr, typing.Dict]


class RabbitFileLogger:
    LOGS_FOLDER = 'rabbit'

    class InternalLogger:
        def __init__(self, logs_folder: typing.AnyStr = None):
            self.LOGS_FOLDER = logs_folder

        def info(self, message: LoggerMessageBase = None):
            try:
                message['type'] = LoggerMessageTypeEnum.INTEGRATION_EVENT.value
                message['details']['event_body'] = json.loads(message['details']['event_body'])
                file_name = os.path.join(self.LOGS_FOLDER, message['details']['name'] + "_" + datetime.now().strftime(
                    "%Y-%m-%dT%H-%M-%S") + ".json")
                with open(file_name, 'w') as json_file:
                    json.dump(message, json_file)
            except Exception as e:
                pass

    def __init__(self, **kwargs):
        if not os.path.exists(self.LOGS_FOLDER):
            os.makedirs(self.LOGS_FOLDER)
        self.logger = self.InternalLogger(self.LOGS_FOLDER)
