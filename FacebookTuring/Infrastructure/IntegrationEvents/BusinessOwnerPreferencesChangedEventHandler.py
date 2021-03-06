import json
import typing

from FacebookTuring.Infrastructure.IntegrationEvents.BusinessOwnerPreferencesChangedEvent import \
    BusinessOwnerPreferencesChangedEvent
from FacebookTuring.Infrastructure.IntegrationEvents.BusinessOwnerPreferencesChangedEventMapping import \
    BusinessOwnerPreferencesChangedEventMapping
from FacebookTuring.Infrastructure.IntegrationEvents.MessageTypeEnum import UserTypeEnum


import logging

logger = logging.getLogger(__name__)


class BusinessOwnerPreferencesChangedEventHandler:
    __mongo_config = None
    __mongo_repository = None
    __orchestrator = None

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
    def handle(cls, body: typing.Union[typing.Dict, typing.AnyStr], days_to_sync: int = None):
        try:
            body = json.loads(body)
            mapper = BusinessOwnerPreferencesChangedEventMapping(target=BusinessOwnerPreferencesChangedEvent)
            message = mapper.load(body)
        except Exception as e:
            raise e

        # update ad account states
        try:
            cls.__mongo_repository.update_business_owner(message.id, message.ad_accounts, days_to_sync)
        except Exception as e:
            logger.exception(f"Failed to update business owners journal || {repr(e)}")

        # start syncing
        try:
            user_type = UserTypeEnum.get_enum_by_name(message.user_type)
            if not user_type:
                user_type = UserTypeEnum.PAYED
            cls.__orchestrator.run(business_owner_id=message.id, user_type=user_type)
        except Exception as e:
            raise e
