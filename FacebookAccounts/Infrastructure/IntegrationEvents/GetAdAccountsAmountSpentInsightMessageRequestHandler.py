import json
import logging

from FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountSpentHandler import \
    GraphAPIAdAccountSpentHandler
from FacebookAccounts.Infrastructure.IntegrationEvents.GetAdAccountsAmountSpentInsightMessageRequest import \
    GetAdAccountsAmountSpentInsightMessageRequest
from FacebookAccounts.Infrastructure.IntegrationEvents.GetAdAccountsAmountSpentInsightMessageRequestMapping import \
    GetAdAccountsAmountSpentInsightMessageRequestMapping
from FacebookAccounts.Infrastructure.IntegrationEvents.GetAdAccountsAmountSpentInsightMessageResponse import (
    FacebookAdAccountsSpending,
    SpendingPerDay,
)
from FacebookAccounts.Infrastructure.IntegrationEvents.GetAdAccountsAmountSpentInsightMessageResponse import \
    GetAdAccountsAmountSpentInsightMessageResponse

logger = logging.getLogger(__name__)


class GetAdAccountsAmountSpentInsightMessageRequestHandler:
    @classmethod
    def handle(cls, message_body, config, fixtures):
        try:
            if isinstance(message_body, str) or isinstance(message_body, bytes):
                message_body = json.loads(message_body)
            request_mapper = GetAdAccountsAmountSpentInsightMessageRequestMapping(
                GetAdAccountsAmountSpentInsightMessageRequest
            )
            request = request_mapper.load(message_body)

            ad_accounts_amount_spent, _ = GraphAPIAdAccountSpentHandler.handle(request, config, fixtures)

            spending = []
            for ad_account in ad_accounts_amount_spent:
                found_ad_account = False
                for existing_account in spending:
                    if existing_account.ad_account_id == ad_account.ad_account_id:
                        found_ad_account = True
                        existing_account.spendings_per_day.append(
                            SpendingPerDay(ad_account.date, ad_account.amount_spent)
                        )
                        break

                if not found_ad_account:
                    spending.append(
                        FacebookAdAccountsSpending(
                            ad_account_id=ad_account.ad_account_id,
                            business_id=ad_account.business_id,
                            business_name=ad_account.business_name,
                            currency=ad_account.currency,
                            spendings_per_day=[SpendingPerDay(ad_account.date, ad_account.amount_spent)],
                        )
                    )

            response = GetAdAccountsAmountSpentInsightMessageResponse(
                filed_user_id=request.filed_user_id,
                business_owner_facebook_id=request.business_owner_facebook_id,
                spendings=spending,
            )
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
