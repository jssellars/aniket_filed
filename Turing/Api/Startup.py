import json

from kombu import Exchange, Queue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Turing.Api.Config.Config import FacebookConfig
from Turing.Api.Config.Config import MongoConfig
from Turing.Api.Config.Config import RabbitMqConfig
from Turing.Api.Config.Config import SQLAlchemyConfig


class Startup(object):

    def __init__(self, appConfig=None):
        assert appConfig is not None

        if not isinstance(appConfig, dict):
            raise ValueError('Invalid app config JSON.')

        self.rabbitmq_config = RabbitMqConfig(appConfig['rabbitmq'])
        self.facebook_config = FacebookConfig(appConfig['facebook'])
        self.database_config = SQLAlchemyConfig(appConfig['sql_server_database'])
        self.mongo_config = MongoConfig(appConfig['mongo_database'])

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
        self.environment = appConfig['environment']
        self.service_name = appConfig['service_name']
        self.service_version = appConfig['service_version']
        self.api_name = appConfig['api_name']
        self.api_version = appConfig['api_version']
        self.base_url = appConfig['base_url']

    def create_sql_session(self):
        return sessionmaker(bind=self.engine)


#  Initialize startup object
with open('Config/Settings/app.settings.dev.json', 'r') as app_settings_json_file:
    app_config = json.load(app_settings_json_file)
startup = Startup(app_config)

jwt_secret_key = "79f4b7c8ff6c919a5c0efc23c7b5f47975ec0d11cef5016a42422521cb62929d32690d8c3b8751dca49c61c0623763c5e5fb98382cf96b85d788fe2638ffbf12"
