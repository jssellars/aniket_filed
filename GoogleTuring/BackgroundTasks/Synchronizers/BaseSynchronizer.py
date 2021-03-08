from Core.Web.GoogleAdWordsAPI.AdWordsAPI.AdWordsBaseClient import AdWordsBaseClient
from Core.settings_models import Mongo


class BaseSynchronizer:
    def __init__(self, business_owner_id: str, account_id: str, adwords_client: AdWordsBaseClient, mongo_config: Mongo):
        self._business_owner_id = business_owner_id
        self._account_id = account_id
        self._adwords_client = adwords_client
        self._mongo_config = mongo_config

    def synchronize(self):
        raise NotImplementedError()
