import logging
from enum import Enum

from Core.Tools.Misc.EnumerationBase import EnumerationBase


class LoggingLevelEnum(EnumerationBase):
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    ERROR = logging.ERROR


class LoggerModeEnum(Enum):
    DEVELOPMENT = 1
    PRODUCTION = 2
