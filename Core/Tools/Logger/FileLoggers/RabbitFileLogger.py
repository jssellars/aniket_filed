import json
import os
import typing
from datetime import datetime
from threading import Thread

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageTypeEnum
from Core.Tools.Misc.Constants import FILENAME_DATETIME

RabbitMessageType = typing.Union[typing.AnyStr, typing.Dict]


class RabbitFileLogger:
    PATH_TO_LOGS = ['..', '..', 'logs', 'Python']
    LOGS_FOLDER = 'rabbit'
    _instance = None

    class InternalLogger:
        def __init__(self, logs_folder: typing.AnyStr = None):
            self.LOGS_FOLDER = logs_folder

        def info(self, message: typing.Dict = None):
            try:
                message['type'] = LoggerMessageTypeEnum.INTEGRATION_EVENT.value
                if isinstance(message['details']['event_body'], str) or \
                        isinstance(message['details']['event_body'], bytes):
                    message['details']['event_body'] = json.loads(message['details']['event_body'])
                else:
                    message['details']['event_body'] = message['details']['event_body']
                file_name = message['details']['name'] + datetime.now().strftime(FILENAME_DATETIME) + ".json"
                file_name = os.path.join(self.LOGS_FOLDER, file_name)
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

            name = kwargs.get('name', '')
            self.LOGS_FOLDER = os.path.join(*self.PATH_TO_LOGS, name, self.LOGS_FOLDER)

            if not os.path.exists(RabbitFileLogger.LOGS_FOLDER):
                os.makedirs(RabbitFileLogger.LOGS_FOLDER)
            self.logger = RabbitFileLogger.InternalLogger(RabbitFileLogger.LOGS_FOLDER)

        return self._instance
