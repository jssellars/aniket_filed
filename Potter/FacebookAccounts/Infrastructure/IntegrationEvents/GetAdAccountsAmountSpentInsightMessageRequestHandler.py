from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from Potter.FacebookAccounts.BackgroundTasks.Startup import startup
from Potter.FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountSpentHandler import GraphAPIAdAccountSpentHandler
from Potter.FacebookAccounts.Infrastructure.IntegrationEvents.GetAdAccountsAmountSpentInsightMessageRequest import GetAdAccountsAmountSpentInsightMessageRequest
from Potter.FacebookAccounts.Infrastructure.IntegrationEvents.GetAdAccountsAmountSpentInsightMessageRequestMapping import GetAdAccountsAmountSpentInsightMessageRequestMapping
from Potter.FacebookAccounts.Infrastructure.IntegrationEvents.GetAdAccountsAmountSpentInsightMessageResponse import GetAdAccountsAmountSpentInsightMessageResponse


class GetAdAccountsAmountSpentInsightMessageRequestHandler:

    @classmethod
    def handle(cls, message_body):
        # map request
        request_mapper = GetAdAccountsAmountSpentInsightMessageRequestMapping(GetAdAccountsAmountSpentInsightMessageRequest)
        request = request_mapper.load(message_body)

        ad_accounts_amount_spent, _ = GraphAPIAdAccountSpentHandler.handle(request)

        response = GetAdAccountsAmountSpentInsightMessageResponse(filed_user_id=request.filed_user_id,
                                                                  user_id=request.user_id,
                                                                  ad_accounts_amount_spent=ad_accounts_amount_spent)
        cls.publish(response)

    @classmethod
    def publish(cls, response):
        # todo: take this out into a base handler class
        try:
            rabbitmq_client = RabbitMqClient(startup.rabbitmq_config, startup.exchange_details.name, startup.exchange_details.outbound_queue.key)
            rabbitmq_client.publish(response)
        except Exception as e:
            raise e