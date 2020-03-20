import json

from kombu import Exchange, Queue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Turing.Config.Config import FacebookConfig
from Turing.Config.Config import MongoConfig
from Turing.Config.Config import RabbitMqConfig
from Turing.Config.Config import SQLAlchemyConfig


class Startup(object):

    def __init__(self, appConfig=None):
        assert appConfig is not None

        if not isinstance(appConfig, dict):
            raise ValueError('Invalid app config JSON.')

        self.rabbitmqConfig = RabbitMqConfig(appConfig['rabbitmq'])
        self.facebookConfig = FacebookConfig(appConfig['facebook'])
        self.databaseConfig = SQLAlchemyConfig(appConfig['sql_server_database'])
        self.mongoConfig = MongoConfig(appConfig['mongo_database'])

        # Initialize connections to DB
        self.engine = create_engine(self.databaseConfig.connection_string)
        self.Session = sessionmaker(bind=self.engine)

        # Initialize RabbitMQ exchanges and queues
        directExchangeConfig = self.rabbitmqConfig.GetExchangeDetailsByType("direct")

        self.directExchange = Exchange(directExchangeConfig['name'],
                                       type=directExchangeConfig['type'])
        queueDetails = directExchangeConfig['queues']
        self.directInboundQueue = Queue(queueDetails['inbound'],
                                        self.directExchange,
                                        routing_key=queueDetails['inbound_routing_key'])
        self.directOutboundQueue = {'name': queueDetails['outbound'],
                                    'key': queueDetails['outbound_routing_key']}

        fanoutExchangeConfig = self.rabbitmqConfig.GetExchangeDetailsByType("fanout")
        self.fanoutExchange = Exchange(fanoutExchangeConfig['name'],
                                       type=fanoutExchangeConfig['type'])

        # Generic msrv configuration
        self.environment = appConfig['environment']
        self.serviceName = appConfig['service_name']
        self.serviceVersion = appConfig['service_version']
        self.apiName = appConfig['api_name']
        self.apiVersion = appConfig['api_version']
        self.baseUrl = appConfig['base_url']

    def CreateSqlSession(self):
        return sessionmaker(bind=self.engine)

#  Initialize startup object
#with open('Config/Settings/app.settings.dev.json', 'r') as app_settings_json_file:
with open('/Users/luchicla/Work/Filed/Source/Filed.Turing/Filed.Turing.BackgroundTasks/Config/Settings/app.settings.dev.json', 'r') as appSettingsJsonFile:
    appConfig = json.load(appSettingsJsonFile)
startup = Startup(appConfig)