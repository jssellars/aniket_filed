import json
import os
import typing
from datetime import datetime
from pathlib import Path
from threading import Thread

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageTypeEnum
from Core.Tools.Misc.Constants import FILENAME_DATETIME

RabbitMessageType = typing.Union[typing.AnyStr, typing.Dict]


class RabbitFileLogger:
    DEFAULT_LOG_ROOT = Path('logs')
    LOCAL_LOG_DIR = 'rabbit'

    _instance = None

    class InternalLogger:
        def __init__(self, log_dir_path: typing.AnyStr = None):
            self.log_dir_path = log_dir_path

        def info(self, message: typing.Dict = None):
            try:
                message['type'] = LoggerMessageTypeEnum.INTEGRATION_EVENT.value
                if isinstance(message['details']['event_body'], (str, bytes)):
                    message['details']['event_body'] = json.loads(message['details']['event_body'])
                file_name = f"{message['details']['name']}{datetime.now().strftime(FILENAME_DATETIME)}.json"

                file_path = self.log_dir_path / file_name
                t = Thread(target=write_json_to_file, args=(file_path, message))
                t.start()
            except Exception as e:
                pass

    def __new__(
            cls,
            name: typing.AnyStr = None,
            level: typing.AnyStr = None,
            index_name: typing.AnyStr = None,
            **kwargs
    ):
        if cls._instance is None:
            cls._instance = super(RabbitFileLogger, cls).__new__(cls)

            cls.name = name

            log_root = os.environ.get('LOG_NETWORK_MOUNT_PATH')
            log_path = Path(log_root) if log_root else cls.DEFAULT_LOG_ROOT
            log_path = log_path / "Python" / name / cls.LOCAL_LOG_DIR

            log_path.mkdir(parents=True, exist_ok=True)

            cls.logger = cls.InternalLogger(cls.LOCAL_LOG_DIR)

        return cls._instance


def write_json_to_file(file_path, message):
    with open(file_path, 'w') as f:
        json.dump(message, f)
