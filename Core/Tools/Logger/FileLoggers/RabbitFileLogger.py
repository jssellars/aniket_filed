import json
import os
import typing
from datetime import datetime
from threading import Thread

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageTypeEnum

RabbitMessageType = typing.Union[typing.AnyStr, typing.Dict]


class RabbitFileLogger:
    LOGS_FOLDER = 'rabbit'
    _instance = None

    class InternalLogger:
        def __init__(self, logs_folder: typing.AnyStr = None):
            self.LOGS_FOLDER = logs_folder

        def info(self, message: typing.Dict = None):
            try:
                message['type'] = LoggerMessageTypeEnum.INTEGRATION_EVENT.value
                message['details']['event_body'] = json.loads(message['details']['event_body']) \
                    if isinstance(message['details']['event_body'], str) or \
                       isinstance(message['details']['event_body'], bytes) \
                    else message['details']['event_body']
                file_name = os.path.join(self.LOGS_FOLDER, message['details']['name'] + "_" + datetime.now().strftime(
                    "%Y-%m-%dT%H-%M-%S") + ".json")
                t = Thread(target=self.save_to_file_async, args=(file_name, message))
                t.start()
            except Exception as e:
                pass

        def save_to_file_async(self, file_name, message):
            json_file = open(file_name, 'w')
            json.dump(message, json_file)
            json_file.close()

    def __new__(self, **kwargs):
        if self._instance is None:
            self._instance = super(RabbitFileLogger, self).__new__(self)

            if not os.path.exists(RabbitFileLogger.LOGS_FOLDER):
                os.makedirs(RabbitFileLogger.LOGS_FOLDER)
            self.logger = RabbitFileLogger.InternalLogger(RabbitFileLogger.LOGS_FOLDER)

        return self._instance
