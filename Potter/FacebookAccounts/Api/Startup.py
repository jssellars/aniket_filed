import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Core.Tools.Config.BaseConfig import ExchangeDetails, QueueDetails
from Potter.FacebookAccounts.Api.Config.Config import RabbitMqConfig, FacebookConfig, SQLAlchemyConfig, ExternalServicesConfig, AdminUserConfig


class Startup(object):

    def __init__(self, app_config=None):
        assert app_config is not None

        if not isinstance(app_config, dict):
            raise ValueError('Invalid app config JSON.')

        self.rabbitmq_config = RabbitMqConfig(app_config['rabbitmq'])
        self.facebook_config = FacebookConfig(app_config['facebook'])
        self.database_config = SQLAlchemyConfig(app_config['sql_server_database'])
        self.external_services = ExternalServicesConfig(app_config["external_services"])
        self.admin_user = AdminUserConfig(app_config["admin_user"])

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
        self.jwt_secret_key = app_config["jwt_secret_key"]
        self.debug_mode = app_config["debug_mode"]

    def create_sql_connection(self):
        return sessionmaker(bind=self.engine)


#  Initialize startup object
env = os.environ.get("PYTHON_ENV")
if not env:
    env = "local"
config_file = f"Config/Settings/app.settings.{env}.json"

with open(config_file, 'r') as app_settings_json_file:
    app_config = json.load(app_settings_json_file)

startup = Startup(app_config)
