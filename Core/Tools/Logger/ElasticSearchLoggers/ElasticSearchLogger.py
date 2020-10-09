import logging
import typing

from cmreslogging.handlers import CMRESHandler

from Core.Tools.Logger.LoggingLevelEnum import LoggingLevelEnum


class ElasticSearchLogger:
    _instance = None

    def __new__(cls,
                host: typing.AnyStr = None,
                port: int = None,
                name: typing.AnyStr = None,
                level: typing.AnyStr = None,
                index_name: typing.AnyStr = None,
                **kwargs):
        if cls._instance is None:
            cls._instance = super(ElasticSearchLogger, cls).__new__(cls)
            cls.host = host
            cls.port = port
            cls.name = name
            cls.level = LoggingLevelEnum.get_enum_by_name(level).value
            cls.es_index = index_name
            cls.logger = ElasticSearchLogger.__init_logger(cls)

        return cls._instance

    def __init_logger(self):
        handler = CMRESHandler(hosts=[{'host': self.host, 'port': self.port}],
                               auth_type=CMRESHandler.AuthType.NO_AUTH,
                               index_name_frequency=CMRESHandler.IndexNameFrequency.DAILY,
                               es_index_name=self.es_index,
                               es_doc_type='_doc',
                               raise_on_indexing_exceptions=True,
                               flush_frequency_in_sec=5)
        handler.setLevel(self.level)
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        logger.addHandler(handler)

        return logger
