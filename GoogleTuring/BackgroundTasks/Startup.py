import json
import os

from kombu import Exchange, Queue

from Core.logging_legacy import LOGGERS_BY_NAME, app_config_as_log_dict
from GoogleTuring.BackgroundTasks.Config.Config import GoogleConfig, MongoConfig, RabbitMqConfig


class Startup:

    def __init__(self, config=None):
        assert config is not None

        if not isinstance(config, dict):
            raise ValueError('Invalid app config JSON.')

        self.rabbitmq_config = RabbitMqConfig(config['rabbitmq'])
        self.google_config = GoogleConfig(config['google'])
        self.mongo_config = MongoConfig(config['mongo_database'])

        # Initialize RabbitMQ exchanges and queues
        direct_exchange_config = self.rabbitmq_config.get_exchange_details_by_type("direct")

        self.direct_exchange = Exchange(direct_exchange_config['name'],
                                        type=direct_exchange_config['type'])
        queue_details = direct_exchange_config['queues']
        self.direct_inbound_queue = Queue(queue_details['inbound'],
                                          self.direct_exchange)

        self.sync_time = app_config["sync_time"]

        # Generic msrv configuration
        self.environment = config['environment']
        self.service_name = config['service_name']
        self.service_version = config['service_version']
        self.api_name = config['api_name']
        self.api_version = config['api_version']
        self.base_url = config['base_url']

        self.docker_filename = app_config["docker_filename"]
        self.logger_type = app_config["logger_type"]
        self.rabbit_logger_type = app_config["rabbit_logger_type"]
        self.logger_level = app_config["logger_level"]
        self.es_host = app_config.get("es_host", None)
        self.es_port = app_config.get("es_port", None)


#  Initialize startup object
env = os.environ.get("PYTHON_ENV")
if not env:
    env = "local"
config_file = f"Config/Settings/app.settings.{env}.json"

with open(config_file, 'r') as app_settings_json_file:
    app_config = json.load(app_settings_json_file)

startup = Startup(app_config)

# Initialize logger
logger = LOGGERS_BY_NAME.get(startup.logger_type)(host=startup.es_host,
                                                  port=startup.es_port,
                                                  name=startup.api_name,
                                                  level=startup.logger_level,
                                                  index_name=startup.docker_filename)

rabbit_logger = LOGGERS_BY_NAME.get(startup.rabbit_logger_type)(host=startup.es_host,
                                                                port=startup.es_port,
                                                                name=startup.api_name,
                                                                level=startup.logger_level,
                                                                index_name=startup.docker_filename)

# Log startup details
logger.logger.info(app_config_as_log_dict(app_config))

