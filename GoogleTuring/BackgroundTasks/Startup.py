from kombu import Exchange, Queue

from GoogleTuring.BackgroundTasks.Config.Config import GoogleConfig, MongoConfig, RabbitMqConfig


class Startup:
    def __init__(self, app_config):
        self.rabbitmq_config = RabbitMqConfig(app_config["rabbitmq"])
        self.google_config = GoogleConfig(app_config["google"])
        self.mongo_config = MongoConfig(app_config["mongo_database"])

        # Initialize RabbitMQ exchanges and queues
        direct_exchange_config = self.rabbitmq_config.get_exchange_details_by_type("direct")

        self.direct_exchange = Exchange(direct_exchange_config["name"], type=direct_exchange_config["type"])
        queue_details = direct_exchange_config["queues"]
        self.direct_inbound_queue = Queue(queue_details["inbound"], self.direct_exchange)

        self.sync_time = app_config["sync_time"]

        self.base_url = app_config["base_url"]
        self.environment = app_config["environment"]
        self.es_host = app_config.get("es_host")
        self.es_port = app_config.get("es_port")
        self.logger_level = app_config["logger_level"]
        self.name = app_config["name"]
        self.version = app_config["version"]


from Core import settings
from Core import logging_config

startup = Startup(settings.config_as_dict)

logging_config.init(
    startup.name, startup.logger_level, enable_es=False, es_host=startup.es_host, es_port=startup.es_port
)
logger = logging_config.get_logger(__name__)

logger.info("Configuration details", extra=logging_config.app_config_as_log_dict(config=settings.config_as_dict))
