import logging
import os
import typing
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from Core.Tools.Logger.FileLoggers.CustomJsonFormatter import CustomJsonFormatter
from Core.Tools.Logger.LoggingLevelEnum import LoggingLevelEnum


class FileLogger:
    LOGS_FOLDER = 'logs'
    DAY = 24 * 3600
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
            self.file_name = os.path.join(self.LOGS_FOLDER, index_name + datetime.now().strftime("%Y-%m-%d") + ".log")

            if not os.path.exists(self.LOGS_FOLDER):
                os.makedirs(self.LOGS_FOLDER)

            self.logger = FileLogger.init_logger(self)

        return self._instance

    def init_logger(self):
        # define logs format
        formatter = CustomJsonFormatter('(level):(name)')

        # create a file handler to log to file
        handler = TimedRotatingFileHandler(self.file_name,
                                           when='midnight', interval=self.DAY)
        handler.setLevel(self.level)
        handler.setFormatter(formatter)

        # create a logger and add the file handler to it
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        logger.addHandler(handler)

        return logger
