from google.ads.googleads.client import GoogleAdsClient
from yaml import dump

from Core.Web.GoogleAdsAPI.AdsAPI.Enums.AdsServiceType import AdsServiceType


class AdsBaseClient:
    def __init__(self, config, refresh_token=None, manager_id=None):
        self._config = config
        self._refresh_token = refresh_token
        self._manager_id = manager_id

        if refresh_token is None:
            self._client = GoogleAdsClient.load_from_storage(path=config.client_config_path)
        else:
            self._client = self.__init_client_with_client_info()

    def __init_client_with_client_info(self):
        config_yaml = {
            "refresh_token": self._refresh_token,
            "developer_token": self._config.developer_token,
            "client_id": self._config.client_id,
            "client_secret": self._config.client_secret,
            "login_customer_id": self._manager_id,
        }

        return GoogleAdsClient.load_from_string(dump(config_yaml))

    def get_location_criterion_service(self):
        return self._client.get_service(AdsServiceType.LOCATION_CRITERION_SERVICE.value)

    def get_budget_service(self):
        return self._client.get_service(AdsServiceType.BUDGET_SERVICE.value)

    def get_customer_service(self):
        return self._client.get_service(AdsServiceType.CUSTOMER_SERVICE.value)

    def get_campaign_service(self):
        return self._client.get_service(AdsServiceType.CAMPAIGN_SERVICE.value)

    def get_ad_group_service(self):
        return self._client.get_service(AdsServiceType.AD_GROUP_SERVICE.value)

    def get_ad_group_ad_service(self):
        return self._client.get_service(AdsServiceType.AD_GROUP_AD_SERVICE.value)

    def get_ad_service(self):
        return self._client.get_service(AdsServiceType.AD_SERVICE.value)

    def get_ad_group_criterion_service(self):
        return self._client.get_service(AdsServiceType.AD_GROUP_CRITERION_SERVICE.value)

    def get_campaign_criterion_service(self):
        return self._client.get_service(AdsServiceType.CAMPAIGN_CRITERION_SERVICE.value)

    def get_search_google_ads_request_type(self):
        return self._client.get_type(AdsServiceType.SEARCH_GOOGLE_ADS_REQUEST.value)

    # def set_client_customer_id(self, client_customer_id):
    #     self._client.set_login_customer(client_customer_id)
