class BaseSynchronizer:
    def __init__(self, business_owner_id, account_id, adwords_client, mongo_config):
        self._business_owner_id = business_owner_id
        self._account_id = account_id
        self._adwords_client = adwords_client
        self._mongo_config = mongo_config

    def synchronize(self):
        raise NotImplementedError()
