import logging

from google.ads.googleads.errors import GoogleAdsException

from GoogleTuring.Infrastructure.GoogleAdsAPI.StructuresClient import StructuresClient

logger = logging.getLogger(__name__)


class AdsAPIStructuresHandler:
    @classmethod
    def _build_client(cls, config, refresh_token, manager_id=None):
        client = StructuresClient(config=config, refresh_token=refresh_token, manager_id=manager_id)
        # TODO look into setting login_customer_id method in ads API
        # ads_client.set_client_customer_id(int(manager_id))
        return client

    @classmethod
    def update_structure(cls, config, refresh_token, command, level):
        client_manager_id = command.client_manager_id
        client_customer_id = command.client_customer_id
        campaign_id = command.campaign_id
        ad_group_id = command.ad_group_id
        keyword_id = command.keyword_id
        edit_details = command.edit_details

        structures_client = cls._build_client(config, refresh_token, client_manager_id)

        try:
            return structures_client.update_structure(
                customer_id=client_customer_id,
                edit_details=edit_details,
                level=level,
                campaign_id=campaign_id,
                ad_group_id=ad_group_id,
                keyword_id=keyword_id,
            )
        except GoogleAdsException as ex:
            logger.exception(f"Request with ID '{ex.request_id}' failed with status {ex.error.code().name}")
