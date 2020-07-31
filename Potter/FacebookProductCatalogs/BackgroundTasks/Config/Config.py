from string import Template

from Core.Tools.Config.BaseConfig import BaseConfig


class FacebookConfig(BaseConfig):
    """Configuration for Facebook Graph API SDK"""
    pass


class RabbitMqConfig(BaseConfig):
    """Configuration for RabbitMQ Client"""

    _MINIMUM_PUBLISH_INTERVAL = 5
    _MINIMUM_HEARTBEAT_ = 4
    _DEFAULT_SERIALIZER_ = 'json'

    @property
    def connection_string(self):
        url = Template('amqp://$user:$password@$host:$port/$vhost')
        return url.substitute(user=self.username,
                              password=self.password,
                              host=self.hostname,
                              port=self.port,
                              vhost=self.virtual_host)

    def get_exchange_details_by_name(self, exchange_name):
        return next(filter(lambda x: x["name"] == exchange_name, self.exchanges), None)

    def get_exchange_details_by_type(self, exchange_type):
        return next(filter(lambda x: x["type"] == exchange_type, self.exchanges), None)


class SQLAlchemyConfig(BaseConfig):
    """Configuration for SQL Alchemy"""

    connection_string_template = Template('mssql+pymssql://$username:$password@$host:$port/$database')

    @property
    def connection_string(self):
        connection_string = self.connection_string_template.substitute(username=self.username,
                                                                       password=self.password,
                                                                       host=self.host,
                                                                       port=self.port,
                                                                       database=self.name)
        return connection_string
