import os
import json

from Core.Tools.Logger.LoggerFactory import LoggerFactory
from Core.Tools.Logger.LoggerMessageStartup import LoggerMessageStartup
from FacebookDexter.Api.Config.Config import MongoConfig, ExternalServicesConfig


class Startup(object):

    def __init__(self, app_config=None):
        assert app_config is not None

        if not isinstance(app_config, dict):
            raise ValueError('Invalid app config JSON.')

        self.mongo_config = MongoConfig(app_config['mongo_database'])
        self.external_services = ExternalServicesConfig(app_config['external_services'])

        self.api_name = app_config['api_name']
        self.api_version = app_config['api_version']
        self.environment = app_config['environment']
        self.port = app_config["port"]
        self.debug = app_config["debug_mode"]
        self.base_url = app_config["base_url"]
        self.logger_type = app_config["logger_type"]
        self.es_host = app_config["es_host"]
        self.es_port = app_config["es_port"]
        self.logger_level= app_config["logger_level"]
        self.docker_filename = app_config["docker_filename"]
        self.jwt_secret_key = app_config["jwt_secret_key"]


# initialize startup object
env = os.environ.get("PYTHON_ENV")
if not env:
    env = "dev"
config_file = os.path.join(os.getcwd(), f"Config/Settings/app.settings.{env}.json")

with open(config_file, 'r') as app_settings_json_file:
    app_config = json.load(app_settings_json_file)

startup = Startup(app_config)

# initialize logger
logger = LoggerFactory.get(startup.logger_type)(host=startup.es_host,
                                                port=startup.es_port,
                                                name=startup.api_name,
                                                level=startup.logger_level,
                                                index_name=startup.docker_filename)

# Log startup details
startup_log = LoggerMessageStartup(app_config=app_config, description="Dexter Recommendations API")
logger.logger.info(startup_log.to_dict())
