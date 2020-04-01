import json
import os

from kombu import Exchange, Queue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Turing.Api.Config.Config import FacebookConfig
from Turing.Api.Config.Config import MongoConfig
from Turing.Api.Config.Config import RabbitMqConfig
from Turing.Api.Config.Config import SQLAlchemyConfig


class Startup(object):

    def __init__(self, app_config=None):
        assert app_config is not None

        if not isinstance(app_config, dict):
            raise ValueError('Invalid app config JSON.')

        self.rabbitmq_config = RabbitMqConfig(app_config['rabbitmq'])
        self.facebook_config = FacebookConfig(app_config['facebook'])
        self.database_config = SQLAlchemyConfig(app_config['sql_server_database'])
        self.mongo_config = MongoConfig(app_config['mongo_database'])

        # Initialize connections to DB
        self.engine = create_engine(self.database_config.connection_string)
        self.Session = sessionmaker(bind=self.engine)

        # Initialize RabbitMQ exchanges and queues
        direct_exchange_config = self.rabbitmq_config.get_exchange_details_by_type("direct")

        self.direct_exchange = Exchange(direct_exchange_config['name'],
                                        type=direct_exchange_config['type'])
        queue_details = direct_exchange_config['queues']
        self.directInboundQueue = Queue(queue_details['inbound'],
                                        self.direct_exchange,
                                        routing_key=queue_details['inbound_routing_key'])
        self.directOutboundQueue = {'name': queue_details['outbound'],
                                    'key': queue_details['outbound_routing_key']}

        fanout_exchange_config = self.rabbitmq_config.get_exchange_details_by_type("fanout")
        self.fanout_exchange = Exchange(fanout_exchange_config['name'],
                                        type=fanout_exchange_config['type'])

        # Generic msrv configuration
        self.environment = app_config['environment']
        self.service_name = app_config['service_name']
        self.service_version = app_config['service_version']
        self.api_name = app_config['api_name']
        self.api_version = app_config['api_version']
        self.base_url = app_config['base_url']
        self.port = app_config["port"]
        self.jwt_secret_key = app_config["jwt_secret_key"]
        self.debug_mode = app_config["debug_mode"]

    def create_sql_session(self):
        return sessionmaker(bind=self.engine)


#  Initialize startup object
env = os.environ.get("PYTHON_ENV")
if not env:
    env = "local"
config_file = f"Config/Settings/app.settings.{env}.json"

with open(config_file, 'r') as app_settings_json_file:
    app_config = json.load(app_settings_json_file)

startup = Startup(app_config)
