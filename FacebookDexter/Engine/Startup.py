import json

from kombu import Exchange, Queue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Config.Config import FacebookConfig
from Config.Config import MongoConfig
from Config.Config import RabbitMqConfig
from Config.Config import SQLAlchemyConfig


class Startup(object):

    def __init__(self, appConfig=None):
        assert appConfig is not None

        if not isinstance(appConfig, dict):
            raise ValueError('Invalid app config JSON.')

        self.rabbitmqConfig = RabbitMqConfig(appConfig['rabbitmq'])
        self.facebookConfig = FacebookConfig(appConfig['facebook'])
        self.databaseConfig = SQLAlchemyConfig(appConfig['sqlServerDatabase'])
        self.mongoConfig = MongoConfig(appConfig['mongoDatabase'])

        # Initialize connections to DB
        self.engine = create_engine(self.databaseConfig.connection_string)
        self.Session = sessionmaker(bind=self.engine)

        # Initialize RabbitMQ exchanges and queues
        directExchangeConfig = self.rabbitmqConfig.get_exchange_details_by_type("direct")

        self.directExchange = Exchange(directExchangeConfig['name'],
                                       type=directExchangeConfig['type'])
        queueDetails = directExchangeConfig['queues']
        self.directInboundQueue = Queue(queueDetails['inbound'],
                                        self.directExchange,
                                        routing_key=queueDetails['inboundRoutingKey'])
        self.directOutboundQueue = {'name': queueDetails['outbound'],
                                    'key': queueDetails['outboundRoutingKey']}

        fanoutExchangeConfig = self.rabbitmqConfig.get_exchange_details_by_type("fanout")
        self.fanoutExchange = Exchange(fanoutExchangeConfig['name'],
                                       type=fanoutExchangeConfig['type'])

        # Generic msrv configuration
        self.runVerbose = appConfig['runVerbose']
        self.logErrors = appConfig['logErrors']
        self.environment = appConfig['environment']
        self.serviceName = appConfig['serviceName']
        self.serviceVersion = appConfig['serviceVersion']
        self.apiName = appConfig['apiName']
        self.apiVersion = appConfig['apiVersion']
        self.baseUrl = appConfig['baseUrl']

    def CreateSqlSession(self):
        return sessionmaker(bind=self.engine)

#  Initialize startup object
#with open('Config/Settings/app.settings.dev.json', 'r') as appSettingsJsonFile:
with open(r'Config/app.settings.dev2.json', 'r') as appSettingsJsonFile:
    appConfig = json.load(appSettingsJsonFile)
startup = Startup(appConfig)