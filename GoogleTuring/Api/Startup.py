import json
import os

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


#  Initialize startup object
env = os.environ.get("PYTHON_ENV")
if not env:
    env = "local"
config_file = f"Config/Settings/app.settings.{env}.json"

with open(config_file, 'r') as app_settings_json_file:
    app_config = json.load(app_settings_json_file)

startup = Startup(app_config)
