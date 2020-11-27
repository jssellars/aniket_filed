import json
import logging
import os
import random
import string
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from threading import Thread
from typing import Dict, Union, TYPE_CHECKING

from cmreslogging.handlers import CMRESHandler
from flask import request
from pythonjsonlogger import jsonlogger

from Core.Tools.Misc.Constants import FILENAME_DATETIME, DEFAULT_DATETIME_ISO

if TYPE_CHECKING:
    from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase


class RabbitFileLogger:
    DEFAULT_LOG_ROOT = Path("logs")
    LOCAL_LOG_DIR = "rabbitmq"

    _instance = None

    class InternalLogger:
        def __init__(self, log_dir_path: str = None):
            self.log_dir_path = log_dir_path

        def info(self, message: Dict = None):
            try:
                message["type"] = logging.getLevelName(logging.INFO)
                if isinstance(message["details"]["event_body"], (str, bytes)):
                    message["details"]["event_body"] = json.loads(message["details"]["event_body"])
                file_name = f"{message['details']['name']}{datetime.now().strftime(FILENAME_DATETIME)}.json"

                file_path = self.log_dir_path / file_name
                t = Thread(target=write_json_to_file, args=(str(file_path), message))
                t.start()
            except:
                pass

    def __new__(cls, name: str = None, level: str = None, index_name: str = None, **kwargs):
        if cls._instance is not None:
            return cls._instance

        cls._instance = super().__new__(cls)
        cls.name = name

        log_root = os.environ.get("LOG_NETWORK_MOUNT_PATH")
        log_path = Path(log_root) if log_root else cls.DEFAULT_LOG_ROOT
        log_path = log_path / "Python" / name / cls.LOCAL_LOG_DIR

        log_path.mkdir(parents=True, exist_ok=True)

        cls.logger = cls.InternalLogger(log_path)

        return cls._instance


def write_json_to_file(file_path, message):
    with open(file_path, "w") as f:
        json.dump(message, f)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    mimetype = "application/json"

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        if not log_record.get("timestamp"):
            # this doesn't use record.created, so it is slightly off
            log_record["@timestamp"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        log_record["level"] = log_record["level"].upper() if log_record.get("level") else record.levelname


class FileLogger:
    DEFAULT_LOG_ROOT = Path("logs")
    LOCAL_LOG_DIR = "logs"

    _instance = None

    def __new__(cls, name: str = None, level: str = None, index_name: str = None, **kwargs):
        if cls._instance is not None:
            return cls._instance

        cls._instance = super().__new__(cls)

        cls.name = name
        cls.level = logging.getLevelName(level)

        log_root = os.environ.get("LOG_NETWORK_MOUNT_PATH")
        log_path = Path(log_root) if log_root else cls.DEFAULT_LOG_ROOT
        log_path = log_path / "Python" / cls.name / cls.LOCAL_LOG_DIR

        cls.file_name = log_path / index_name
        log_path.mkdir(parents=True, exist_ok=True)

        suffixed_file_name = f"{cls.file_name}.log"
        handler = TimedRotatingFileHandler(suffixed_file_name, when="MIDNIGHT")
        handler.namer = lambda name: f"{name.replace(suffixed_file_name, str(cls.file_name))}.log"
        handler.setLevel(cls.level)
        handler.setFormatter(CustomJsonFormatter("(level):(name)"))

        logger = logging.getLogger(cls.name)
        logger.addHandler(handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter("[{asctime}] [{levelname}] {message}", style="{"))
        logger.addHandler(stream_handler)

        logger.setLevel(cls.level)

        cls.logger = logger

        return cls._instance


class ElasticSearchLogger:
    _instance = None

    def __new__(
        cls, host: str = None, port: int = None, name: str = None, level: str = None, index_name: str = None, **kwargs,
    ):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.host = host
            cls.port = port
            cls.name = name
            cls.level = logging.getLevelName(level)
            cls.es_index = index_name
            cls.logger = ElasticSearchLogger.__init_logger(cls)

        return cls._instance

    def __init_logger(self):
        handler = CMRESHandler(
            hosts=[{"host": self.host, "port": self.port}],
            auth_type=CMRESHandler.AuthType.NO_AUTH,
            index_name_frequency=CMRESHandler.IndexNameFrequency.DAILY,
            es_index_name=self.es_index,
            es_doc_type="_doc",
            raise_on_indexing_exceptions=True,
            flush_frequency_in_sec=5,
        )
        handler.setLevel(self.level)
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        logger.addHandler(handler)

        return logger


# todo: this should be refactored and redone. it's not functional
class MongoLogger:
    _instance = None

    class Logger:
        COLLECTION_NAME = "logs"

        def __init__(self, repository: "MongoRepositoryBase" = None, database_name: str = None):
            self.__repository = repository.new_repository()
            self.__repository.set_database(database_name)
            self.__repository.set_collection(self.COLLECTION_NAME)

        def info(self, message: Dict = None):
            self.__repository.add_one(message)

    def __new__(self, repository: "MongoRepositoryBase" = None, database_name: str = None):
        if self._instance is None:
            self._instance = super().__new__(self)

        self.logger = MongoLogger.Logger(repository, database_name)

        return self._instance


__MONGO_REQUEST_ID_LENGTH__ = 20


def log_operation_mongo(
    request_id=None,
    logger=None,
    log_level=None,
    data=None,
    description=None,
    timestamp=None,
    duration=None,
    query=None,
    projection=None,
    query_filter=None,
):
    # don't attempt to log anything if no logger is provided
    if logger is None:
        return

    if not request_id:
        request_id = "".join(random.choice(string.ascii_lowercase) for _ in range(__MONGO_REQUEST_ID_LENGTH__))
    log_extra_data = dict(request_id=request_id, timestamp=timestamp.strftime(DEFAULT_DATETIME_ISO), duration=duration)
    if logger.level == logging.DEBUG:
        log_extra_data.update(
            data_size=sys.getsizeof(data), query=query, query_filter=query_filter, projection=projection,
        )
    log = log_message_as_dict(
        mtype=log_level, name="MongoDB Database Operation", description=description, extra_data=log_extra_data
    )
    if log_level == logging.ERROR:
        logger.logger.exception(log)
    else:
        logger.logger.info(log)

    return request_id


LOGGERS_BY_NAME = {
    "file_logger": FileLogger,
    "elasticsearch_logger": ElasticSearchLogger,
    "rabbit_file_logger": RabbitFileLogger,
    "rabbit_elasticsearch_logger": ElasticSearchLogger,
}


def request_as_log_dict(r: request):
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


def request_as_log_dict_nested(r: request):
    return dict(details=request_as_log_dict(r))


RABBIT_KEYS = ["username", "hostname", "port", "virtual_host", "exchanges"]
MONGO_KEYS = ["mongo_host", "remote_ip", "remote_port"]
SQL_KEYS = ["host", "port", "database"]
FACEBOOK_KEYS = ["description", "api_version"]


def app_config_as_log_dict(config: Dict):
    mongo_config = config.get("mongo_database", {})
    all_mongo_keys = MONGO_KEYS + [i for i in mongo_config if "database" in i or "collection" in i]

    return {
        "details": {
            "service_name": config.get("service_name"),
            "environment": config.get("environment"),
            "api_name": config.get("api_name"),
            "api_version": config.get("api_version"),
            "service_version": config.get("service_version"),
            "port": config.get("port"),
            "debug_mode": config.get("debug_mode"),
            "rabbit": {k: config.get("rabbitmq", {}).get(k) for k in RABBIT_KEYS},
            "mongo": {k: mongo_config.get(k) for k in all_mongo_keys},
            "tokens_database": {k: config.get("sql_server_database", {}).get(k) for k in SQL_KEYS},
            "facebook": {k: config.get("facebook", {}).get(k) for k in FACEBOOK_KEYS},
            "external_services": config.get("external_services", {}),
        }
    }


def log_message_as_dict(
    mtype: int = logging.NOTSET,
    name: str = None,
    code: int = None,
    description: str = None,
    extra_data: Union[str, Dict] = None,
) -> Dict:
    details = dict(
        type=logging.getLevelName(mtype),
        name=name,
        code=code,
        description=description,
    )
    try:
        if extra_data:
            details.update(extra_data)
    except Exception as e:
        details.update(error=f"Failed to generate log {e}")

    return dict(details=details)
