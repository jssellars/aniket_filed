from Core.Web.Security.Authorization import authorize_permission, authorize_jwt
from GoogleTuring.Api.Config.Config import MongoConfig, GoogleConfig


class Startup:
    def __init__(self, app_config):
        self.mongo_config = MongoConfig(app_config["mongo_database"])
        self.google_config = GoogleConfig(app_config["google"])

        self.__auth_permission_endpoint = app_config["external_services"]["authorize_permission_endpoint"]

        self.base_url = app_config["base_url"]
        self.environment = app_config["environment"]
        self.es_host = app_config.get("es_host")
        self.es_port = app_config.get("es_port")
        self.logger_level = app_config["logger_level"]
        self.name = app_config["name"]
        self.port = app_config["port"]
        self.version = app_config["version"]

    @property
    def authorize_permission(self):
        return authorize_permission(self.__auth_permission_endpoint)

    @property
    def authorize_jwt(self):
        return authorize_jwt(self.__auth_permission_endpoint)


from Core import settings
from Core import logging_config

startup = Startup(settings.config_as_dict)

logging_config.init(
    startup.name, startup.logger_level, enable_es=False, es_host=startup.es_host, es_port=startup.es_port
)
logger = logging_config.get_logger(__name__)

logger.info("Configuration details", extra=logging_config.app_config_as_log_dict(config=settings.config_as_dict))
