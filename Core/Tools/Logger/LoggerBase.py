import typing

from flask import request

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerFactory import LoggerType


def log_request_data_handler(logger: LoggerType = None, api_request: request = None) -> typing.NoReturn:
    request_log = LoggerAPIRequestMessageBase(api_request)
    logger.logger.info(request_log.to_dict())
