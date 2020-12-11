import typing

from FacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPIPixelsHandler import GraphAPIPixelHandler
from FacebookPixels.Infrastructure.IntegrationEvents.GetAllPixelsMessageRequest import \
    GetAllPixelsMessageRequest
from FacebookPixels.Infrastructure.IntegrationEvents.GetAllPixelsMessageRequestMapping import \
    GetAllPixelsMessageRequestMapping
from FacebookPixels.Infrastructure.IntegrationEvents.GetAllPixelsMessageResponse import \
    GetAllPixelsMessageResponse


import logging

logger = logging.getLogger(__name__)


class GetAllPixelsMessageRequestHandler:
    @classmethod
    def handle(cls, message_body: typing.Dict, config, fixtures) -> typing.NoReturn:
        try:
            message_mapper = GetAllPixelsMessageRequestMapping(target=GetAllPixelsMessageRequest)
            message = message_mapper.load(message_body)

            permanent_token = fixtures.business_owner_repository.get_permanent_token(message.business_owner_facebook_id)

            pixels, errors = GraphAPIPixelHandler.get_pixels(permanent_token=permanent_token,
                                                             account_id=message.ad_account_id, config=config)

            response = GetAllPixelsMessageResponse(business_owner_facebook_id=message.business_owner_facebook_id,
                                                   ad_account_id=message.ad_account_id,
                                                   pixels=pixels,
                                                   errors=errors)
            cls.__publish(response, fixtures)
        except Exception as e:
            raise e

    @classmethod
    def __publish(cls, pixels, fixtures):
        try:
            rabbitmq_adapter = fixtures.rabbitmq_adapter
            rabbitmq_adapter.publish(pixels)
            logger.info({"rabbitmq": rabbitmq_adapter.serialize_message(pixels)})
        except Exception as e:
            raise e
