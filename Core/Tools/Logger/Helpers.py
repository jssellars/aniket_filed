import random
import string
import sys

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.Logger.LoggingLevelEnum import LoggingLevelEnum
from Core.Tools.Misc.Constants import DEFAULT_DATETIME_ISO

__MONGO_REQUEST_ID_LENGTH__ = 20


def log_operation_mongo(request_id=None,
                        logger=None,
                        log_level=None,
                        data=None,
                        description=None,
                        timestamp=None,
                        duration=None,
                        query=None,
                        projection=None,
                        query_filter=None):
    # don't attempt to log anything if no logger is provided
    if logger is None:
        return

    if not request_id:
        request_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(__MONGO_REQUEST_ID_LENGTH__))
    if logger.level == LoggingLevelEnum.DEBUG.value:
        log_extra_data = {
            "request_id": request_id,
            "data_size": sys.getsizeof(data),
            "timestamp": timestamp.strftime(DEFAULT_DATETIME_ISO),
            "duration": duration,
            "query": query,
            "query_filter": query_filter,
            "projection": projection
        }
    else:
        log_extra_data = {
            "request_id": request_id,
            "timestamp": timestamp.strftime(DEFAULT_DATETIME_ISO),
            "duration": duration
        }

    log = LoggerMessageBase(mtype=log_level,
                            name="MongoDB Database Operation",
                            description=description,
                            extra_data=log_extra_data)
    if log_level == LoggerMessageTypeEnum.ERROR:
        logger.logger.exception(log.to_dict())
    else:
        logger.logger.info(log.to_dict())

    return request_id
