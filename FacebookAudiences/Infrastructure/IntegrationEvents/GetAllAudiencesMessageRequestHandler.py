import json
import logging

from FacebookAudiences.Infrastructure.GraphAPIHandlers.GraphAPIAudiencesHandler import GraphAPIAudiencesHandler
from FacebookAudiences.Infrastructure.IntegrationEvents.GetAllAudiencesMessageRequest import (
    GetAllAudiencesMessageRequest,
)
from FacebookAudiences.Infrastructure.IntegrationEvents.GetAllAudiencesMessageRequestMapping import (
    GetAllAudiencesMessageRequestMapping,
)
from FacebookAudiences.Infrastructure.IntegrationEvents.GetAllAudiencesMessageResponse import (
    GetAllAudiencesMessageResponse,
)

logger = logging.getLogger(__name__)


class GetAllAudiencesMessageRequestHandler:
    @classmethod
    def handle(cls, message_body: str, config, fixtures) -> None:
        try:
            message_body = json.loads(message_body)

            message_mapper = GetAllAudiencesMessageRequestMapping(target=GetAllAudiencesMessageRequest)
            message = message_mapper.load(message_body)

            permanent_token = fixtures.business_owner_repository.get_permanent_token(message.business_owner_facebook_id)

            audiences, errors = GraphAPIAudiencesHandler.get_audiences(
                permanent_token=permanent_token, account_id=message.ad_account_id, config=config
            )

            response = GetAllAudiencesMessageResponse(
                business_owner_facebook_id=message.business_owner_facebook_id,
                ad_account_id=message.ad_account_id,
                business_id=message.business_id,
                audiences=audiences,
                errors=errors,
            )

            cls.__publish(response, fixtures)
        except Exception as e:
            raise e

    @classmethod
    def __publish(cls, response: GetAllAudiencesMessageResponse, fixtures) -> None:
        try:
            rabbitmq_adapter = fixtures.rabbitmq_adapter
            rabbitmq_adapter.publish(response)
            logger.info({"rabbitmq": rabbitmq_adapter.serialize_message(response)})
        except Exception as e:
            raise e
