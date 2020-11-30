import json
import typing

from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from FacebookAudiences.BackgroundTasks.Startup import startup
from FacebookAudiences.Infrastructure.GraphAPIHandlers.GraphAPIAudiencesHandler import GraphAPIAudiencesHandler
from FacebookAudiences.Infrastructure.IntegrationEvents.GetAllAudiencesMessageRequest import \
    GetAllAudiencesMessageRequest
from FacebookAudiences.Infrastructure.IntegrationEvents.GetAllAudiencesMessageRequestMapping import \
    GetAllAudiencesMessageRequestMapping
from FacebookAudiences.Infrastructure.IntegrationEvents.GetAllAudiencesMessageResponse import \
    GetAllAudiencesMessageResponse


import logging

logger = logging.getLogger(__name__)


class GetAllAudiencesMessageRequestHandler:
    @classmethod
    def handle(cls, message_body: typing.AnyStr) -> typing.NoReturn:
        try:
            message_body = json.loads(message_body)

            #  load message
            message_mapper = GetAllAudiencesMessageRequestMapping(target=GetAllAudiencesMessageRequest)
            message = message_mapper.load(message_body)

            # get permanent token
            permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(
                message.business_owner_facebook_id)

            # get audiences
            audiences, errors = GraphAPIAudiencesHandler.get_audiences(permanent_token=permanent_token,
                                                                       account_id=message.ad_account_id,
                                                                       startup=startup)

            response = GetAllAudiencesMessageResponse(business_owner_facebook_id=message.business_owner_facebook_id,
                                                      ad_account_id=message.ad_account_id,
                                                      business_id=message.business_id,
                                                      audiences=audiences,
                                                      errors=errors)

            cls.__publish(response)
        except Exception as e:
            raise e

    @classmethod
    def __publish(cls, response: GetAllAudiencesMessageResponse) -> typing.NoReturn:
        try:
            rabbitmq_client = RabbitMqClient(startup.rabbitmq_config,
                                             startup.exchange_details.name,
                                             startup.exchange_details.outbound_queue.key)
            rabbitmq_client.publish(response)
            logger.info({"rabbitmq": rabbitmq_client.serialize_message(response)})
        except Exception as e:
            raise e
