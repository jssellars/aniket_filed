import typing

from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Potter.FacebookAccounts.BackgroundTasks.Startup import startup
from Potter.FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountHandler import GraphAPIAdAccountHandler
from Potter.FacebookAccounts.Infrastructure.IntegrationEvents.GetBusinessOwnersTreesMessageRequest import GetBusinessOwnersTreesMessageRequest
from Potter.FacebookAccounts.Infrastructure.IntegrationEvents.GetBusinessOwnersTreesMessageRequestMapping import GetBusinessOwnersTreesMessageRequestMapping
from Potter.FacebookAccounts.Infrastructure.IntegrationEvents.GetBusinessOwnersTreesMessageResponse import GetBusinessOwnersTreesMessageResponse


class GetBusinessOwnersTreesMessageRequestHandler:

    @classmethod
    def handle(cls, message_body: typing.Dict):
        # map message_body dict to object
        mapping = GetBusinessOwnersTreesMessageRequestMapping(GetBusinessOwnersTreesMessageRequest)
        request = mapping.load(message_body)

        # get business owner permanent token
        for business_owner in request.business_owners:
            business_owner_permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(business_owner.facebook_id)

            graph_api_handler = GraphAPIAdAccountHandler(business_owner_permanent_token, startup.facebook_config)
            businesses = graph_api_handler.get_business_owner_details(business_owner.facebook_id)

            response = GetBusinessOwnersTreesMessageResponse(facebook_id=business_owner.facebook_id, businesses=businesses)
            cls.publish(response)

    @classmethod
    def publish(cls, response):
        try:
            rabbitmq_client = RabbitMqClient(startup.rabbitmq_config, startup.exchange_details.name, startup.exchange_details.outbound_queue.key)
            rabbitmq_client.publish(response)
        except Exception as e:
            raise e