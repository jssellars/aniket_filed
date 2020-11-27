import logging
from logging import handlers
import os
from pathlib import Path
from typing import Any, Optional, Mapping

from cmreslogging.handlers import CMRESHandler

import requests

logging.getLogger("requests").setLevel(logging.WARNING)


LOG_FORMAT = "{asctime} {levelname} {name}:{lineno} || {message}"
LOG_FORMAT_VERBOSE = "{asctime} {levelname} {name}:{module}:{funcName}:{lineno} || {message}"
LOG_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_FORMATTER = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATETIME_FORMAT, style="{")


# TODO: see if we can use this, disabled for now since it can't help with extra dict
# old_record_factory = logging.getLogRecordFactory()
#
#
# def record_factory(*args, **kwargs):
#     record = old_record_factory(*args, **kwargs)
#     record.custom_attribute = "custom"
#
#     return record
#
#
# logging.setLogRecordFactory(record_factory)


class ExtraLogger(logging.Logger):
    def makeRecord(
        self,
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: Any,
        args: Any,
        exc_info: Optional[Any],
        func: Optional[str] = None,
        extra: Optional[Mapping[str, Any]] = None,
        sinfo: Optional[str] = None,
    ) -> logging.LogRecord:
        rv = logging.getLogRecordFactory()(name, level, fn, lno, msg, args, exc_info, func, sinfo)
        # keep original functionality but save extra as a standalone dict for easy structured output
        if extra and isinstance(extra, dict):
            rv.__dict__["extra"] = {}
            for key in extra:
                if (key in ["message", "asctime"]) or (key in rv.__dict__):
                    raise KeyError("Attempt to overwrite %r in LogRecord" % key)
                rv.__dict__["extra"][key] = extra[key]

            for key, value in rv.extra.items():
                rv.__dict__[key] = value

            # keep the original message for structured handlers which will use the extra dict
            rv.msg_orig = rv.msg
            rv.msg += f" || {rv.extra}"
            # TODO: see if pretty format is better
            # rv.msg += " || " + " ~~ ".join(f"{k}::{v}" for k, v in rv.extra.items())

        return rv


logging.setLoggerClass(ExtraLogger)


# TODO: see if we need the filter for corner cases, otherwise remove
class ExtraDataFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        extra_data = getattr(record, "extra_data", {})
        if extra_data:
            record.msg += f" || {extra_data}"

        return True


class RabbitFilter(logging.Filter):
    def __init__(self, *, hide_rabbits: bool = False):
        super().__init__()
        self.hide_rabbits = hide_rabbits

    def filter(self, record: logging.LogRecord) -> bool:
        # TODO: see if this is needed
        # if isinstance(message["details"]["event_body"], (str, bytes)):
        #     message["details"]["event_body"] = json.loads(message["details"]["event_body"])

        # to qualify as rabbit data, a dict with a rabbitmq key must be supplied as message or extra
        rabbit_data = getattr(record, "rabbitmq", record.msg.get("rabbitmq") if isinstance(record.msg, dict) else None)

        if not self.hide_rabbits and rabbit_data:
            record.msg = str(rabbit_data)
            return True

        if self.hide_rabbits and not rabbit_data:
            return True

        return False


def init(service_name: str, level_name: str, enable_es: bool = False, es_host: str = "localhost", es_port: int = 9200):
    """
    Examples:
        Regular:
            root_logger.info("A message")
        RabbitMQ:
            root_logger.info("A message", extra=dict(rabbitmq=dict(a=1, b=2)))
            root_logger.info(dict(rabbitmq=dict(a=1, b=2)))
    """
    # root_logger = logging.RootLogger(logging.DEBUG)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.getLevelName(level_name))
    # disabled because filters re not inherited
    # root_logger.addFilter(ExtraDataFilter())

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(DEFAULT_FORMATTER)
    stream_handler.addFilter(RabbitFilter(hide_rabbits=True))
    root_logger.addHandler(stream_handler)

    root_dir = os.environ.get("LOG_NETWORK_MOUNT_PATH")
    service_path = Path(root_dir if root_dir else "logs") / "py" / service_name
    service_path.mkdir(parents=True, exist_ok=True)

    app_handler = get_timed_rotating_file_handler(str(service_path / "app"))
    app_handler.addFilter(RabbitFilter(hide_rabbits=True))
    root_logger.addHandler(app_handler)

    rabbitmq_handler = get_timed_rotating_file_handler(str(service_path / "rabbitmq"))
    rabbitmq_handler.addFilter(RabbitFilter())
    root_logger.addHandler(rabbitmq_handler)

    if enable_es:
        es_handler = CMRESHandler(
            hosts=[dict(host=es_host, port=es_port)],
            auth_type=CMRESHandler.AuthType.NO_AUTH,
            index_name_frequency=CMRESHandler.IndexNameFrequency.DAILY,
            es_index_name=f"py-{service_name.replace('.', '-')}",
            es_doc_type="_doc",
            raise_on_indexing_exceptions=True,
            flush_frequency_in_sec=5,
        )
        root_logger.addHandler(es_handler)


def get_timed_rotating_file_handler(file_path: str) -> handlers.TimedRotatingFileHandler:
    suffixed_file_path = f"{file_path}.log"
    handler = handlers.TimedRotatingFileHandler(suffixed_file_path, when="MIDNIGHT")
    handler.namer = lambda name: f"{name.replace(suffixed_file_path, file_path)}.log"
    handler.setFormatter(DEFAULT_FORMATTER)
    # handler.setFormatter(CustomJsonFormatter("(level):(name)"))

    return handler


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
