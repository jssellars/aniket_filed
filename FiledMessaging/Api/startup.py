from Core import fixtures
from Core import logging_config
from FiledMessaging.Api import settings

config = settings.core.get_settings(settings, settings.core.get_environment())
fixtures = fixtures.Fixtures(config)
logging_config.init(config)
logger = logging_config.get_logger(__name__)
logger.info(
    "Configuration details", extra=logging_config.app_config_as_log_dict(config)
)
