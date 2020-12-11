import logging
from datetime import datetime
from logging import handlers
import os
from pathlib import Path
from typing import Any, Optional, Mapping, TYPE_CHECKING, Dict

from cmreslogging.handlers import CMRESHandler
from flask import request
from pythonjsonlogger import jsonlogger

from Core.settings import Model

if TYPE_CHECKING:
    from Core import settings

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("pika").setLevel(logging.WARNING)


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
        # to qualify as rabbit data, a dict with a rabbitmq key must be supplied as message or extra
        rabbit_data = getattr(record, "rabbitmq", record.msg.get("rabbitmq") if isinstance(record.msg, dict) else None)

        if not self.hide_rabbits and rabbit_data:
            record.msg = str(rabbit_data)
            return True

        if self.hide_rabbits and not rabbit_data:
            return True

        return False


class MongoHandler(logging.Handler):
    def __init__(self, config: "settings.Mongo"):
        super().__init__()

        from Core.mongo_adapter import MongoRepositoryBase

        self._repository = MongoRepositoryBase.new_logs_repository(config)

    def emit(self, record):
        self._repository.add_one(record.msg)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    mimetype = "application/json"

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        if not log_record.get("timestamp"):
            # this doesn't use record.created, so it is slightly off
            log_record["@timestamp"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")


# TODO: !!! use UTC time instead of local as in the previously used CustomJsonFormatter !!!
def init(config: Model):
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
    root_logger.setLevel(logging.getLevelName(config.logger_level))
    # disabled because filters re not inherited
    # root_logger.addFilter(ExtraDataFilter())

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(DEFAULT_FORMATTER)
    stream_handler.addFilter(RabbitFilter(hide_rabbits=True))
    root_logger.addHandler(stream_handler)

    root_dir = os.environ.get("LOG_NETWORK_MOUNT_PATH")
    service_path = Path(root_dir if root_dir else "logs") / "py" / config.name.full
    service_path.mkdir(parents=True, exist_ok=True)

    app_handler = get_timed_rotating_file_handler(str(service_path / "app"))
    app_handler.addFilter(RabbitFilter(hide_rabbits=True))
    root_logger.addHandler(app_handler)

    rabbitmq_handler = get_timed_rotating_file_handler(str(service_path / "rabbitmq"))
    rabbitmq_handler.addFilter(RabbitFilter())
    root_logger.addHandler(rabbitmq_handler)

    if config.es_enabled:
        es_handler = CMRESHandler(
            hosts=[dict(host=config.es_host, port=config.es_port)],
            auth_type=CMRESHandler.AuthType.NO_AUTH,
            index_name_frequency=CMRESHandler.IndexNameFrequency.DAILY,
            es_index_name=f"py-{config.name.full.replace('.', '-')}",
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


RABBIT_KEYS = ["username", "hostname", "port", "virtual_host", "exchanges"]
MONGO_KEYS = ["ssh_host", "mongo_host_internal", "mongo_port"]
SQL_KEYS = ["host", "port", "database"]
FACEBOOK_KEYS = ["description", "api_version"]


def app_config_as_log_dict(config: Model):
    mongo_config = config.mongo.dict()
    all_mongo_keys = MONGO_KEYS + [i for i in mongo_config if "database" in i or "collection" in i]

    return {
        "environment": config.environment,
        "app_name": config.name.full,
        "app_version": config.version,
        "port": config.port,
        "rabbit": {k: config.rabbitmq.dict().get(k) for k in RABBIT_KEYS},
        "mongo": {k: mongo_config.get(k) for k in all_mongo_keys},
        "tokens_database": {k: config.sql_server.dict().get(k) for k in SQL_KEYS},
        "facebook": {k: config.facebook.dict().get(k) for k in FACEBOOK_KEYS},
        "external_services": config.external_services,
    }


def request_as_log_dict(r: request) -> Dict:
    return dict(
        method=r.method,
        base_url=r.base_url,
        endpoint=r.endpoint,
        full_path=r.full_path,
        remote_address=r.remote_addr,
        payload=r.get_data(),
        # === WARNING === only activate this log if it is really needed ===
        # headers=r.headers,
    )
