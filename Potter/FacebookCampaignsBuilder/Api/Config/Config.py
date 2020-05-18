from string import Template

from Core.Tools.Config.BaseConfig import BaseConfig


class FacebookConfig(BaseConfig):
    """Configuration for Facebook Graph API SDK"""
    pass


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
