from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Core.Tools.Config.BaseConfig import ExchangeDetails, QueueDetails
from FacebookApps.BackgroundTasks.Config.Config import RabbitMqConfig, FacebookConfig, SQLAlchemyConfig


class Startup:
    def __init__(self, app_config):
        self.rabbitmq_config = RabbitMqConfig(app_config["rabbitmq"])
        self.facebook_config = FacebookConfig(app_config["facebook"])
        self.database_config = SQLAlchemyConfig(app_config["sql_server_database"])

        # Initialize connections to DB
        self.engine = create_engine(self.database_config.connection_string)
        self.session = sessionmaker(bind=self.engine)

        # Initialize RabbitMQ exchanges and queues
        direct_exchange_config = self.rabbitmq_config.get_exchange_details_by_type("direct")
        self.exchange_details = ExchangeDetails(
            name=direct_exchange_config["name"], type=direct_exchange_config["type"]
        )
        self.exchange_details.inbound_queue = QueueDetails(
            direct_exchange_config["queues"]["inbound"], direct_exchange_config["queues"]["inbound_routing_key"]
        )
        self.exchange_details.outbound_queue = QueueDetails(
            direct_exchange_config["queues"]["outbound"], direct_exchange_config["queues"]["outbound_routing_key"]
        )

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
