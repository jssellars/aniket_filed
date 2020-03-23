from io import StringIO

from googleads import adwords
from yaml import safe_load, dump


class AdWordsBaseClient:
    def __init__(self, config, client_customer_id=None, refresh_token=None, client_id=None, client_secret=None):
        self._config = config
        self._client_customer_id = client_customer_id
        self._refresh_token = refresh_token
        self._client_id = client_id
        self._client_secret = client_secret

        if client_id is None:
            self._client = adwords.AdWordsClient.LoadFromStorage(path=config.client_config_path)
        else:
            self._client = self.__init_client_with_client_info()

    def __init_client_with_client_info(self):
        stream_data = StringIO()
        with open(self._config.client_config_path, 'r') as fp:
            stream_data.write(fp.read())

        stream_data.seek(0)
        config_yaml = safe_load(stream_data)

        config_yaml['client_customer_id'] = self._client_customer_id
        config_yaml['refresh_token'] = self._refresh_token
        config_yaml['client_id'] = self._client_id
        config_yaml['client_secret'] = self._client_secret

        return adwords.AdWordsClient.LoadFromString(dump(config_yaml))

    def get_report_downloader(self):
        return self._client.GetReportDownloader()

    def get_location_criterion_service(self):
        return self._client.GetService('LocationCriterionService')
