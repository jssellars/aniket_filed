import json

from FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountSpentHandler import \
    GraphAPIAdAccountSpentHandler
from FacebookAccounts.Infrastructure.IntegrationEvents.GetAdAccountsAmountSpentInsightMessageRequest import \
    GetAdAccountsAmountSpentInsightMessageRequest
from FacebookAccounts.Infrastructure.IntegrationEvents.GetAdAccountsAmountSpentInsightMessageRequestMapping import \
    GetAdAccountsAmountSpentInsightMessageRequestMapping
from FacebookAccounts.Infrastructure.IntegrationEvents.GetAdAccountsAmountSpentInsightMessageResponse import \
    GetAdAccountsAmountSpentInsightMessageResponse


import logging

logger = logging.getLogger(__name__)


class GetAdAccountsAmountSpentInsightMessageRequestHandler:
    @classmethod
    def handle(cls, message_body, config, fixtures):
        try:
            if isinstance(message_body, str) or isinstance(message_body, bytes):
                message_body = json.loads(message_body)
            request_mapper = GetAdAccountsAmountSpentInsightMessageRequestMapping(
                GetAdAccountsAmountSpentInsightMessageRequest)
            request = request_mapper.load(message_body)

            ad_accounts_amount_spent, _ = GraphAPIAdAccountSpentHandler.handle(request, config, fixtures)

            response = GetAdAccountsAmountSpentInsightMessageResponse(filed_user_id=request.filed_user_id,
                                                                      user_id=request.user_id,
                                                                      ad_accounts_amount_spent=ad_accounts_amount_spent,
                                                                      from_date=request.from_date,
                                                                      to_date=request.to_date)
        except Exception as e:
            raise e

        cls.publish(response, fixtures)

    @classmethod
    def publish(cls, response, fixtures):
        try:
            rabbitmq_adapter = fixtures.rabbitmq_adapter
            rabbitmq_adapter.publish(response)
            logger.info(response.message_type, extra=dict(rabbitmq=rabbitmq_adapter.serialize_message(response)))
        except Exception as e:
            raise e
