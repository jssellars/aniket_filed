import json
import os

from Core.Tools.Logger.LoggerFactory import LoggerFactory
from GoogleTuring.Api.Config.Config import MongoConfig, GoogleConfig


class Startup(object):
    def __init__(self, app_config=None):
        assert app_config is not None

        if not isinstance(app_config, dict):
            raise ValueError('Invalid app config JSON.')
        self.mongo_config = MongoConfig(app_config['mongo_database'])
        self.google_config = GoogleConfig(app_config['google'])

        # Generic msrv configuration
        self.jwt_secret_key = app_config["jwt_secret_key"]
        self.port = app_config["port"]
        self.debug_mode = app_config["debug_mode"]
        self.environment = app_config['environment']
        self.service_name = app_config['service_name']
        self.service_version = app_config['service_version']
        self.api_name = app_config['api_name']
        self.api_version = app_config['api_version']
        self.base_url = app_config['base_url']

        self.docker_filename = app_config["docker_filename"]
        self.logger_type = app_config["logger_type"]
        self.rabbit_logger_type = app_config["rabbit_logger_type"]
        self.logger_level = app_config["logger_level"]
        self.es_host = app_config.get("es_host", None)
        self.es_port = app_config.get("es_port", None)


#  Initialize startup object
env = os.environ.get("PYTHON_ENV")
if not env:
    env = "dev"
config_file = f"Config/Settings/app.settings.{env}.json"

with open(config_file, 'r') as app_settings_json_file:
    app_config = json.load(app_settings_json_file)

startup = Startup(app_config)

# Initialize logger
logger = LoggerFactory.get(startup.logger_type)(host=startup.es_host,
                                                port=startup.es_port,
                                                name=startup.api_name,
                                                level=startup.logger_level,
                                                index_name=startup.docker_filename)
