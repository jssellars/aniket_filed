from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Core.Tools.Config.BaseConfig import ExchangeDetails, QueueDetails
from Core.logging_legacy import app_config_as_log_dict
from Core.Web.Security.Authorization import authorize_permission, authorize_jwt
from Core.Web.Security.TechnicalTokenManager import TechnicalTokenManager
from FacebookAccounts.Api.Config.Config import RabbitMqConfig, FacebookConfig, SQLAlchemyConfig, \
    ExternalServicesConfig, AdminUserConfig


class Startup(object):
    def __init__(self, app_config=None):
        assert app_config is not None

        if not isinstance(app_config, dict):
            raise ValueError('Invalid app config JSON.')

        self.rabbitmq_config = RabbitMqConfig(app_config['rabbitmq'])
        self.facebook_config = FacebookConfig(app_config['facebook'])
        self.database_config = SQLAlchemyConfig(app_config['sql_server_database'])
        self.external_services = ExternalServicesConfig(app_config["external_services"])
        self.technical_user = AdminUserConfig(app_config["technical_user"])

        self.__auth_permission_endpoint = app_config['external_services']['authorize_permission_endpoint']

        # Initialize connections to DB
        self.engine = create_engine(self.database_config.connection_string)
        self.session = sessionmaker(bind=self.engine)

        # Initialize RabbitMQ exchanges and queues
        direct_exchange_config = self.rabbitmq_config.get_exchange_details_by_type("direct")
        self.exchange_details = ExchangeDetails(name=direct_exchange_config["name"],
                                                type=direct_exchange_config["type"])
        self.exchange_details.inbound_queue = QueueDetails(direct_exchange_config["queues"]["inbound"],
                                                           direct_exchange_config["queues"]["inbound_routing_key"])
        self.exchange_details.outbound_queue = QueueDetails(direct_exchange_config["queues"]["outbound"],
                                                            direct_exchange_config["queues"]["outbound_routing_key"])

        self.environment = app_config['environment']
        self.service_name = app_config['service_name']
        self.service_version = app_config['service_version']
        self.api_name = app_config['api_name']
        self.api_version = app_config['api_version']
        self.base_url = app_config['base_url']
        self.port = app_config["port"]
        self.debug_mode = app_config["debug_mode"]
        self.docker_filename = app_config["docker_filename"]
        self.logger_type = app_config["logger_type"]
        self.rabbit_logger_type = app_config["rabbit_logger_type"]
        self.logger_level = app_config["logger_level"]
        self.es_host = app_config.get("es_host", None)
        self.es_port = app_config.get("es_port", None)
        self.technical_token_manager = TechnicalTokenManager(self.technical_user, self.external_services)

    @property
    def authorize_permission(self):
        return authorize_permission(self.__auth_permission_endpoint)

    @property
    def authorize_jwt(self):
        return authorize_jwt(self.__auth_permission_endpoint)

    def create_sql_connection(self):
        return sessionmaker(bind=self.engine)


from Core import settings

startup = Startup(settings.config_as_dict)

from Core import logging_config

logging_config.init(
    "FacebookAccount.Api", startup.logger_level, enable_es=False, es_host=startup.es_host, es_port=startup.es_port
)
logger = logging_config.get_logger(__name__)

logger.info("Configuration details", extra=app_config_as_log_dict(config=settings.config_as_dict)["details"])
