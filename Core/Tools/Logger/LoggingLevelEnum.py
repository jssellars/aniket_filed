import logging

from Core.Tools.Misc.EnumerationBase import EnumerationBase


class LoggingLevelEnum(EnumerationBase):
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    ERROR = logging.ERROR
