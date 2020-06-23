from io import StringIO

from googleads import adwords
from yaml import safe_load, dump

from Core.Web.GoogleAdWordsAPI.AdWordsAPI.Enums.AdWordsServiceType import AdWordsServiceType


class AdWordsBaseClient:
    _CHUNK_SIZE = 16 * 1024

    def __init__(self, config, refresh_token=None):
        self._config = config
        self._refresh_token = refresh_token

        if refresh_token is None:
            self._client = adwords.AdWordsClient.LoadFromStorage(path=config.client_config_path)
        else:
            self._client = self.__init_client_with_client_info()

    def __init_client_with_client_info(self):
        config_yaml = {'adwords': {}}
        config_yaml['adwords']['refresh_token'] = self._refresh_token
        config_yaml['adwords']['developer_token'] = self._config.developer_token
        config_yaml['adwords']['client_id'] = self._config.client_id
        config_yaml['adwords']['client_secret'] = self._config.client_secret

        return adwords.AdWordsClient.LoadFromString(dump(config_yaml))

    def get_report_downloader(self):
        return self._client.GetReportDownloader()

    def get_location_criterion_service(self):
        return self._client.GetService(AdWordsServiceType.LOCATION_CRITERION_SERVICE.value)

    def get_budget_service(self):
        return self._client.GetService(AdWordsServiceType.BUDGET_SERVICE.value)

    def get_campaign_service(self):
        return self._client.GetService(AdWordsServiceType.CAMPAIGN_SERVICE.value)

    def get_ad_group_service(self):
        return self._client.GetService(AdWordsServiceType.AD_GROUP_SERVICE.value)

    def get_ad_group_ad_service(self):
        return self._client.GetService(AdWordsServiceType.AD_GROUP_AD_SERVICE.value)

    def get_ad_service(self):
        return self._client.GetService(AdWordsServiceType.AD_SERVICE.value)

    def get_ad_group_criterion_service(self):
        return self._client.GetService(AdWordsServiceType.AD_GROUP_CRITERION_SERVICE.value)

    def get_campaign_criterion_service(self):
        return self._client.GetService(AdWordsServiceType.CAMPAIGN_CRITERION_SERVICE.value)

    def set_client_customer_id(self, client_customer_id):
        self._client.SetClientCustomerId(client_customer_id)
