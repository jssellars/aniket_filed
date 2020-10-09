import logging
import os
import typing
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from Core.Tools.Logger.FileLoggers.CustomJsonFormatter import CustomJsonFormatter
from Core.Tools.Logger.LoggingLevelEnum import LoggingLevelEnum


class FileLogger:
    DEFAULT_LOG_ROOT = Path('logs')
    LOCAL_LOG_DIR = 'logs'

    _instance = None

    def __new__(
            cls,
            name: typing.AnyStr = None,
            level: typing.AnyStr = None,
            index_name: typing.AnyStr = None,
            **kwargs
    ):
        if cls._instance is None:
            cls._instance = super(FileLogger, cls).__new__(cls)

            cls.name = name
            cls.level = LoggingLevelEnum.get_enum_by_name(level).value

            log_root = os.environ.get('LOG_NETWORK_MOUNT_PATH')
            log_path = Path(log_root) if log_root else cls.DEFAULT_LOG_ROOT
            log_path = log_path / "Python" / cls.name / cls.LOCAL_LOG_DIR

            cls.file_name = log_path / index_name
            log_path.mkdir(parents=True, exist_ok=True)
            cls.logger = FileLogger.init_logger(cls)

        return cls._instance

    def init_logger(self):
        # create a file handler to log to file
        suffixed_file_name = f"{self.file_name}.log"
        handler = TimedRotatingFileHandler(suffixed_file_name, when="MIDNIGHT")
        handler.namer = lambda name: f"{name.replace(suffixed_file_name, self.file_name)}.log"
        handler.setLevel(self.level)
        handler.setFormatter(CustomJsonFormatter('(level):(name)'))

        # create a logger and add the file handler to it
        logger = logging.getLogger(self.name)
        logger.addHandler(handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter("[{asctime}] [{levelname}] {message}", style="{"))
        logger.addHandler(stream_handler)

        logger.setLevel(self.level)

        return logger
