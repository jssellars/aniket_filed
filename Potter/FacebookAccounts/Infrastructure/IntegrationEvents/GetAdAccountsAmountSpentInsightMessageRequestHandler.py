import json
import typing

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageTypeEnum, LoggerMessageBase
from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from Potter.FacebookAccounts.BackgroundTasks.Startup import startup
from Potter.FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountSpentHandler import \
    GraphAPIAdAccountSpentHandler
from Potter.FacebookAccounts.Infrastructure.IntegrationEvents.GetAdAccountsAmountSpentInsightMessageRequest import \
    GetAdAccountsAmountSpentInsightMessageRequest
from Potter.FacebookAccounts.Infrastructure.IntegrationEvents.GetAdAccountsAmountSpentInsightMessageRequestMapping import \
    GetAdAccountsAmountSpentInsightMessageRequestMapping
from Potter.FacebookAccounts.Infrastructure.IntegrationEvents.GetAdAccountsAmountSpentInsightMessageResponse import \
    GetAdAccountsAmountSpentInsightMessageResponse


class GetAdAccountsAmountSpentInsightMessageRequestHandler:
    __rabbit_logger = None

    @classmethod
    def set_rabbit_logger(cls, logger: typing.Any):
        cls.__rabbit_logger = logger
        return cls

    @classmethod
    def handle(cls, message_body):
        try:
            if isinstance(message_body, str) or isinstance(message_body, bytes):
                message_body = json.loads(message_body)
            request_mapper = GetAdAccountsAmountSpentInsightMessageRequestMapping(
                GetAdAccountsAmountSpentInsightMessageRequest)
            request = request_mapper.load(message_body)

            ad_accounts_amount_spent, _ = GraphAPIAdAccountSpentHandler.handle(request)

            response = GetAdAccountsAmountSpentInsightMessageResponse(filed_user_id=request.filed_user_id,
                                                                      user_id=request.user_id,
                                                                      ad_accounts_amount_spent=ad_accounts_amount_spent,
                                                                      from_date=request.from_date,
                                                                      to_date=request.to_date)
        except Exception as e:
            raise e

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
