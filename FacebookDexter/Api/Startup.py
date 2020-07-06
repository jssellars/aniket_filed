import os
import json

from Core.Tools.Logger.LoggerFactory import LoggerFactory
from Core.Tools.Logger.LoggerMessageStartup import LoggerMessageStartup
from FacebookDexter.Api.Models.Config.ExternalServices import DexterApiExternalServices
from FacebookDexter.Api.Models.Config.LoggingInfo import DexterApiLoggingInfo


class Startup(object):

    def __init__(self, app_config=None):
        assert app_config is not None

        if not isinstance(app_config, dict):
            raise ValueError('Invalid app config JSON.')

        self.api_name = app_config['api_name']
        self.api_version = app_config['api_version']
        self.environment = app_config['environment']
        self.port = app_config["port"]
        self.debug = app_config["debug_mode"]
        self.base_url = app_config['base_url']
        self.mongo_config = app_config['mongo_database']
        self.external_services = DexterApiExternalServices(app_config['external_services']['facebook_auto_apply'],
                                                           app_config['external_services']['google_auto_apply'])
        self.logging = DexterApiLoggingInfo(self.api_name,
                                            app_config['logging']['logger_type'],
                                            app_config['logging']['es_host'],
                                            app_config['logging']['es_port'],
                                            app_config['logging']['logger_level'],
                                            app_config['logging']['docker_filename'])


env = os.environ.get("PYTHON_ENV")
if not env:
    env = "dev"

config_file = os.path.join(os.getcwd(), f"Config/Settings/app.settings.{env}.json")

with open(config_file, 'r') as app_settings_json_file:
    app_config = json.load(app_settings_json_file)

startup = Startup(app_config)

logger = LoggerFactory.get(startup.logging.logger_type)(host=startup.logging.es_host,
                                                        port=startup.logging.es_port,
                                                        name=startup.api_name,
                                                        level=startup.logging.level,
                                                        index_name=startup.logging.index_name)

# Log startup details
startup_log = LoggerMessageStartup(app_config=app_config, description="Dexter Recommendations API")
logger.logger.info(startup_log.to_dict())
