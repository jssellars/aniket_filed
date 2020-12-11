import json
import typing

from FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountHandler import GraphAPIAdAccountHandler
from FacebookAccounts.Infrastructure.IntegrationEvents.GetBusinessOwnersTreesMessageRequest import \
    BusinessOwner
from FacebookAccounts.Infrastructure.IntegrationEvents.GetBusinessOwnersTreesMessageResponse import \
    GetBusinessOwnersTreesMessageResponse


import logging

logger = logging.getLogger(__name__)


class GetBusinessOwnersTreesMessageRequestHandler:
    @classmethod
    def handle(cls, message_body: typing.Dict, config, fixtures):
        if isinstance(message_body, str) or isinstance(message_body, bytes):
            message_body = json.loads(message_body)
        try:
            for entry in message_body["business_owners"]:
                business_owner = BusinessOwner(**entry)
                cls.__get_business_owner_permanent_token(config, fixtures, business_owner)
        except Exception as e:
            raise e

    @classmethod
    def __get_business_owner_permanent_token(cls, config, fixtures, business_owner: BusinessOwner = None):
        business_owner_permanent_token = fixtures.business_owner_repository.get_permanent_token(
            business_owner.id)

        # TODO: what happens when the BO is not found in the db ?
        if business_owner_permanent_token:
            graph_api_handler = GraphAPIAdAccountHandler(business_owner_permanent_token, config.facebook)
            businesses = graph_api_handler.get_business_owner_details(business_owner.id)

            response = GetBusinessOwnersTreesMessageResponse(facebook_id=business_owner.id, businesses=businesses)
            cls.publish(response, fixtures)

    @classmethod
    def publish(cls, response, fixtures):
        try:
            rabbitmq_adapter = fixtures.rabbitmq_adapter
            rabbitmq_adapter.publish(response)
            logger.info(response.message_type, extra=dict(rabbitmq=rabbitmq_adapter.serialize_message(response)))
        except Exception as e:
            raise e
