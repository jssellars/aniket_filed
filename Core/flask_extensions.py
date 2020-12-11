import functools

from flask import request

from Core.logging_config import request_as_log_dict


def log_request(logger):
    def inner_log_request(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(request_as_log_dict(request))

            return func(*args, **kwargs)

        return wrapper

    return inner_log_request
