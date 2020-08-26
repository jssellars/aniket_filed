import typing

from Core.Dexter.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from Core.Dexter.PersistanceLayer.DexterRecommendationsMongoRepository import DexterRecommendationsMongoRepository


class OrchestratorBuilder:

    def __init__(self):
        self.business_owner_id = None
        self.ad_account_id = None
        self.startup = None
        self.logger = None
        self._channel = None
        self._algorithm_type = None
        self._data_repository = None
        self._recommendations_repository = None
        self._journal_repository = None
        self._auth_token = None

    def set_logger(self, logger: typing.Any = None):
        self.logger = logger

    def set_business_owner_id(self, business_owner_id: typing.AnyStr = None):
        self.business_owner_id = business_owner_id
        return self

    def set_ad_account_id(self, ad_account_id: typing.AnyStr = None):
        self.ad_account_id = ad_account_id
        return self

    def set_startup(self, startup: typing.Any = None):
        self.startup = startup
        return self

    def set_data_repository(self, repository):
        self._data_repository = repository
        return self

    def set_recommendations_repository(self, repository: DexterRecommendationsMongoRepository = None):
        self._recommendations_repository = repository
        return self

    def set_journal_repository(self, repository: DexterJournalMongoRepository = None):
        self._journal_repository = repository
        return self

    def set_auth_token(self, auth_token: typing.AnyStr = None):
        self._auth_token = auth_token
        return self

    @property
    def algorithm_type(self):
        return self._algorithm_type
