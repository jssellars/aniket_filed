import typing

from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Potter.FacebookAudiences.BackgroundTasks.Startup import startup
from Potter.FacebookAudiences.Infrastructure.GraphAPIHandlers.GraphAPIAudiencesHandler import GraphAPIAudiencesHandler
from Potter.FacebookAudiences.Infrastructure.IntegrationEvents.GetAllAudiencesMessageRequest import GetAllAudiencesMessageRequest
from Potter.FacebookAudiences.Infrastructure.IntegrationEvents.GetAllAudiencesMessageRequestMapping import GetAllAudiencesMessageRequestMapping
from Potter.FacebookAudiences.Infrastructure.IntegrationEvents.GetAllAudiencesMessageResponse import GetAllAudiencesMessageResponse


class GetAllAudiencesMessageRequestHandler:

    @classmethod
    def handle(cls, message_body: typing.MutableMapping) -> typing.NoReturn:
        #  load message
        message_mapper = GetAllAudiencesMessageRequestMapping(target=GetAllAudiencesMessageRequest)
        message = message_mapper.load(message_body)

        # get permanent token
        permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(message.business_owner_facebook_id)

        # get audiences
        audiences, errors = GraphAPIAudiencesHandler.get_audiences(permanent_token=permanent_token, account_id=message.ad_account_id, startup=startup)

        #  Publish response details to audiences outbound queue
        # todo: use below after c# changes ErrorMessage
        # response = GetAllAudiencesMessageResponse(ad_account_id=message.ad_account_id, business_id=message.business_id, audiences=audiences, errors=errors)
        response = GetAllAudiencesMessageResponse(business_owner_facebook_id=message.business_owner_facebook_id,
                                                  ad_account_id=message.ad_account_id,
                                                  business_id=message.business_id,
                                                  audiences=audiences,
                                                  errors=[])

        cls.__publish(response)

    @classmethod
    def __publish(cls, response: GetAllAudiencesMessageResponse) -> typing.NoReturn:
        try:
            rabbitmq_client = RabbitMqClient(startup.rabbitmq_config,
                                             startup.exchange_details.name,
                                             startup.exchange_details.outbound_queue.key)
            rabbitmq_client.publish(response)
        except Exception as e:
            raise e
