from string import Template

from Turing.Config.BaseConfig import BaseConfig


class FacebookConfig(BaseConfig):

    __FACEBOOK_PERMISSIONS__ = ['email',
                                'user_link',
                                'user_location',
                                'user_posts',
                                'user_videos',
                                'ads_management',
                                'ads_read',
                                'business_management',
                                'manage_pages',
                                'pages_manage_cta',
                                'pages_show_list',
                                'user_events',
                                'instagram_basic',
                                'leads_retrieval',
                                'read_audience_network_insights',
                                'read_insights',
                                'instagram_manage_insights']


class RabbitMqConfig(BaseConfig):

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

    def GetExchangeDetailsByType(self, exchange_type):
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


class MongoConfig(BaseConfig):
    """Configuration for Mongo DB client"""
