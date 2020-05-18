import json
import typing

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from FacebookTuring.Infrastructure.IntegrationEvents.BusinessOwnerPreferencesChangedEvent import \
    BusinessOwnerPreferencesChangedEvent
from FacebookTuring.Infrastructure.IntegrationEvents.BusinessOwnerPreferencesChangedEventMapping import \
    BusinessOwnerPreferencesChangedEventMapping


class BusinessOwnerPreferencesChangedEventHandler:
    __mongo_config = None
    __mongo_repository = None
    __orchestrator = None
    __logger = None

    @classmethod
    def set_logger(cls, logger: typing.Any):
        cls.__logger = logger
        return cls

    @classmethod
    def set_mongo_config(cls, mongo_config: typing.Any = None) -> typing.Any:
        cls.__mongo_config = mongo_config
        return cls

    @classmethod
    def set_mongo_repository(cls, mongo_repository: typing.Any = None) -> typing.Any:
        cls.__mongo_repository = mongo_repository
        return cls

    @classmethod
    def set_orchestrator(cls, orchestrator: typing.Any = None) -> typing.Any:
        cls.__orchestrator = orchestrator
        return cls

    @classmethod
    def handle(cls, body: typing.Union[typing.Dict, typing.AnyStr]):
        try:
            body = json.loads(body)
            mapper = BusinessOwnerPreferencesChangedEventMapping(target=BusinessOwnerPreferencesChangedEvent)
            message = mapper.load(body)
        except Exception as e:
            raise e

        # update ad account states
        try:
            cls.__mongo_repository.update_business_owner(message.id, message.ad_accounts)
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="Failed to update business owners journal",
                                    description=str(e))
            cls.__logger.logger.exception(log.to_dict())

        # start syncing
        try:
            cls.__orchestrator.run()
        except Exception as e:
            raise e
