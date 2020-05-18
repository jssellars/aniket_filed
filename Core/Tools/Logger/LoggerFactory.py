import typing

from Core.Tools.Logger.ElasticSearchLoggers.ElasticSearchLogger import ElasticSearchLogger
from Core.Tools.Logger.FileLoggers.FileLogger import FileLogger
from Core.Tools.Logger.FileLoggers.RabbitFileLogger import RabbitFileLogger

LoggerType = typing.Union[ElasticSearchLogger, FileLogger, typing.NoReturn]


class LoggerFactory:
    __loggers = {
        "file_logger": FileLogger,
        "elasticsearch_logger": ElasticSearchLogger,
        "rabbit_file_logger": RabbitFileLogger,
        "rabbit_elasticsearch_logger": ElasticSearchLogger
    }

    @classmethod
    def get(cls, logger_type: typing.AnyStr = None) -> LoggerType:
        return cls.__loggers.get(logger_type, None)
