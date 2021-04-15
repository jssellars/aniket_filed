import logging

from google.ads.googleads.errors import GoogleAdsException

from GoogleAccounts.Infrastructure.GoogleAdsAPI.AdAccountInsightsClient import AdAccountInsightsClient

logger = logging.getLogger(__name__)


class AdAccountInsightsCommandHandler:
    @classmethod
    def _build_client(cls, config, manager_id, refresh_token):
        ad_account_insights_client = AdAccountInsightsClient(
            config=config, refresh_token=refresh_token, manager_id=manager_id
        )
        # TODO look into setting login_customer_id method in ads API
        # ads_client.set_client_customer_id(int(manager_id))
        return ad_account_insights_client

    @classmethod
    def handle(cls, google_config, command, manager_id):
        REFRESH_TOKEN = (
            "1//0cgG4P2mKtjsMCgYIARAAGAwSNwF-L9Ir0Vl_1PxJPDAfNBcJerYGQEtxvAPuVoecfoJpsm3zedWUdyPRkG-NJk5i-iOFW5uaKaE"
        )
        ad_account_insights_client = cls._build_client(google_config, manager_id, REFRESH_TOKEN)

        try:
            return ad_account_insights_client.get_account_insights(command, manager_id)
        except GoogleAdsException as ex:
            logger.exception(f"Request with ID '{ex.request_id}' failed with status {ex.error.code().name}")
