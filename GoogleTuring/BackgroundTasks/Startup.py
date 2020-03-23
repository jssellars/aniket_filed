import json

from kombu import Exchange, Queue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from GoogleTuring.BackgroundTasks.Config.Config import GoogleConfig, MongoConfig, RabbitMqConfig, SQLAlchemyConfig


class Startup:

    def __init__(self, config=None):
        assert config is not None

        if not isinstance(config, dict):
            raise ValueError('Invalid app config JSON.')

        self.rabbitmq_config = RabbitMqConfig(config['rabbitmq'])
        self.google_config = GoogleConfig(config['google'])
        self.database_config = SQLAlchemyConfig(config['sqlServerDatabase'])
        self.mongo_config = MongoConfig(config['mongoDatabase'])

        # Initialize connections to DB
        self.engine = create_engine(self.database_config.connection_string)
        self.Session = sessionmaker(bind=self.engine)

        # Initialize RabbitMQ exchanges and queues
        direct_exchange_config = self.rabbitmq_config.get_exchange_details_by_type("direct")

        self.direct_exchange = Exchange(direct_exchange_config['name'],
                                        type=direct_exchange_config['type'])
        queue_details = direct_exchange_config['queues']
        self.direct_inbound_queue = Queue(queue_details['inbound'],
                                          self.direct_exchange,
                                          routing_key=queue_details['inbound_routing_key'])
        self.direct_outbound_queue = {'name': queue_details['outbound'],
                                      'key': queue_details['outbound_routing_key']}

        fanout_exchange_config = self.rabbitmq_config.get_exchange_details_by_type("fanout")
        self.fanout_exchange = Exchange(fanout_exchange_config['name'],
                                        type=fanout_exchange_config['type'])

        # Generic msrv configuration
        self.environment = config['environment']
        self.service_name = config['serviceName']
        self.service_version = config['serviceVersion']
        self.api_name = config['apiName']
        self.api_version = config['apiVersion']
        self.base_url = config['baseUrl']

    def create_sql_session(self):
        return sessionmaker(bind=self.engine)


with open(r'Config\Settings\app.settings.dev.json', 'r') as app_settings_json_file:
    app_config = json.load(app_settings_json_file)

startup = Startup(app_config)
