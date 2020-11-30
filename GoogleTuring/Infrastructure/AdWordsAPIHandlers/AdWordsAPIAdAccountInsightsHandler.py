from GoogleTuring.Infrastructure.AdWordsAPIHandlers.AdWordsAPIBaseHandler import AdWordsAPIBaseHandler
from GoogleTuring.Infrastructure.GoogleAdWordsAPI.AdWordsAccountInsightsClient import AdWordsAccountInsightsClient

import logging

logger = logging.getLogger(__name__)


class AdWordsAPIAdAccountInsightsHandler(AdWordsAPIBaseHandler):
    @classmethod
    def _build_client(cls, config, client_customer_id, permanent_token):
        adwords_client = AdWordsAccountInsightsClient(config=config, refresh_token=permanent_token)
        return adwords_client

    @classmethod
    def get_ad_account_insights(cls, config, permanent_token, client_customer_ids, start_date, end_date):
        adwords_client = cls._build_client(config, client_customer_ids, permanent_token)
        ad_account_insights = []
        for client_customer_id in client_customer_ids:
            adwords_client.set_client_customer_id(int(client_customer_id))
            try:
                insights = adwords_client.get_account_insights(start_date=start_date, end_date=end_date)
                ad_account_insights.extend(insights)
            except Exception as e:
                logger.exception(repr(e))

        return ad_account_insights
