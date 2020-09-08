import logging
import os
import typing
from logging.handlers import TimedRotatingFileHandler

from Core.Tools.Logger.FileLoggers.CustomJsonFormatter import CustomJsonFormatter
from Core.Tools.Logger.LoggingLevelEnum import LoggingLevelEnum


class FileLogger:
    LOGS_FOLDER = 'logs'
    _instance = None

    def __new__(self,
                name: typing.AnyStr = None,
                level: typing.AnyStr = None,
                index_name: typing.AnyStr = None,
                **kwargs):
        if self._instance is None:
            self._instance = super(FileLogger, self).__new__(self)

            self.name = name
            self.level = LoggingLevelEnum.get_enum_by_name(level).value
            self.file_name = os.path.join(self.LOGS_FOLDER, index_name)

            os.makedirs(self.LOGS_FOLDER, exist_ok=True)

            self.logger = FileLogger.init_logger(self)

        return self._instance

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

        logger.setLevel(self.level)

        return logger
