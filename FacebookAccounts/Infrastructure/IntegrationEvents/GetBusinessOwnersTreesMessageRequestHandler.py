import json
import typing

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from FacebookAccounts.BackgroundTasks.Startup import startup
from FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountHandler import GraphAPIAdAccountHandler
from FacebookAccounts.Infrastructure.IntegrationEvents.GetBusinessOwnersTreesMessageRequest import \
    BusinessOwner
from FacebookAccounts.Infrastructure.IntegrationEvents.GetBusinessOwnersTreesMessageResponse import \
    GetBusinessOwnersTreesMessageResponse


class GetBusinessOwnersTreesMessageRequestHandler:
    __rabbit_logger = None

    @classmethod
    def set_rabbit_logger(cls, logger: typing.Any):
        cls.__rabbit_logger = logger
        return cls

    @classmethod
    def handle(cls, message_body: typing.Dict):
        if isinstance(message_body, str) or isinstance(message_body, bytes):
            message_body = json.loads(message_body)
        try:
            #  get business owner permanent token
            for entry in message_body["business_owners"]:
                business_owner = BusinessOwner(**entry)
                cls.__get_business_owner_permanent_token(business_owner)
        except Exception as e:
            raise e

    @classmethod
    def __get_business_owner_permanent_token(cls, business_owner: BusinessOwner = None):
        business_owner_permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(
            business_owner.id)

        # TODO: what happens when the BO is not found in the db ?
        if business_owner_permanent_token:
            graph_api_handler = GraphAPIAdAccountHandler(business_owner_permanent_token, startup.facebook_config)
            businesses = graph_api_handler.get_business_owner_details(business_owner.id)

            response = GetBusinessOwnersTreesMessageResponse(facebook_id=business_owner.id, businesses=businesses)
            cls.publish(response)

    @classmethod
    def publish(cls, response):
        try:
            rabbitmq_client = RabbitMqClient(startup.rabbitmq_config, startup.exchange_details.name,
                                             startup.exchange_details.outbound_queue.key)
            rabbitmq_client.publish(response)
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.INTEGRATION_EVENT,
                                    name=response.message_type,
                                    extra_data={"event_body": rabbitmq_client.serialize_message(response)})
            cls.__rabbit_logger.logger.info(log.to_dict())
        except Exception as e:
            raise e
