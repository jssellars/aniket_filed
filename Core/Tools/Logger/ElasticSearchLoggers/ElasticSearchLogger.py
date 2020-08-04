import logging
import typing

from cmreslogging.handlers import CMRESHandler

from Core.Tools.Logger.LoggingLevelEnum import LoggingLevelEnum


class ElasticSearchLogger:
    _instance = None

    def __new__(self,
                 host: typing.AnyStr = None,
                 port: int = None,
                 name: typing.AnyStr = None,
                 level: typing.AnyStr = None,
                 index_name: typing.AnyStr = None,
                 **kwargs):
        if self._instance is None:
            self._instance = super(ElasticSearchLogger, self).__new__(self)
            self.host = host
            self.port = port
            self.name = name
            self.level = LoggingLevelEnum.get_enum_by_name(level).value
            self.es_index = index_name

            self.logger = ElasticSearchLogger.__init_logger(self)

        return self._instance

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
