import logging
import typing
from datetime import datetime

from cmreslogging.handlers import CMRESHandler

from Core.Tools.Logger.LoggingLevelEnum import LoggingLevelEnum


class ElasticSearchLogger:
    def __init__(self,
                 host: typing.AnyStr = None,
                 port: int = None,
                 name: typing.AnyStr = None,
                 level: typing.AnyStr = None,
                 index_name: typing.AnyStr = None,
                 **kwargs):
        self.host = host
        self.port = port
        self.name = name
        self.level = LoggingLevelEnum.get_enum_by_name(level).value
        self.es_index = index_name + "-" + datetime.now().strftime("%Y-%m-%d")

        self.logger = self.__init_logger()

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
