import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Core.Tools.Config.BaseConfig import ExchangeDetails, QueueDetails
from Core.Tools.Logger.LoggerFactory import LoggerFactory
from Core.Tools.Logger.LoggerMessageStartup import LoggerMessageStartup
from Potter.FacebookAccounts.Api.Config.Config import FacebookConfig, SQLAlchemyConfig
from Potter.FacebookCampaignsBuilder.Api.Config.Config import RabbitMqConfig


class Startup(object):

    def __init__(self, app_config=None):
        assert app_config is not None

        if not isinstance(app_config, dict):
            raise ValueError('Invalid app config JSON.')

        self.facebook_config = FacebookConfig(app_config['facebook'])
        self.database_config = SQLAlchemyConfig(app_config['sql_server_database'])
        self.rabbitmq_config = RabbitMqConfig(app_config['rabbitmq'])

        # Initialize connections to DB
        self.engine = create_engine(self.database_config.connection_string)
        self.session = sessionmaker(bind=self.engine)

        # Initialize RabbitMQ exchanges and queues
        direct_exchange_config = self.rabbitmq_config.get_exchange_details_by_type("direct")
        self.exchange_details = ExchangeDetails(name=direct_exchange_config["name"],
                                                type=direct_exchange_config["type"])
        self.exchange_details.outbound_queue = QueueDetails(direct_exchange_config["queues"]["outbound"],
                                                            direct_exchange_config["queues"]["outbound_routing_key"])

        self.environment = app_config['environment']
        self.service_name = app_config['service_name']
        self.service_version = app_config['service_version']
        self.api_name = app_config['api_name']
        self.api_version = app_config['api_version']
        self.base_url = app_config['base_url']
        self.port = app_config["port"]
        self.jwt_secret_key = app_config["jwt_secret_key"]
        self.debug_mode = app_config["debug_mode"]
        self.docker_filename = app_config["docker_filename"]
        self.logger_type = app_config["logger_type"]
        self.rabbit_logger_type = app_config["rabbit_logger_type"]
        self.logger_level = app_config["logger_level"]
        self.es_host = app_config.get("es_host", None)
        self.es_port = app_config.get("es_port", None)


def create_sql_connection(self):
    return sessionmaker(bind=self.engine)


#  Initialize startup object
env = os.environ.get("PYTHON_ENV")
if not env:
    env = "dev"
config_file = f"Config/Settings/app.settings.{env}.json"

with open(config_file, 'r') as app_settings_json_file:
    app_config = json.load(app_settings_json_file)

startup = Startup(app_config)

# Initialize logger
logger = LoggerFactory.get(startup.logger_type)(host=startup.es_host,
                                                port=startup.es_port,
                                                name=startup.api_name,
                                                level=startup.logger_level,
                                                index_name=startup.docker_filename)

rabbit_logger = LoggerFactory.get(startup.rabbit_logger_type)(host=startup.es_host,
                                                              port=startup.es_port,
                                                              name=startup.api_name,
                                                              level=startup.logger_level,
                                                              index_name=startup.docker_filename)

# Log startup details
startup_log = LoggerMessageStartup(app_config=app_config, description="Potter Facebook Campaign Builder API")
logger.logger.info(startup_log.to_dict())
