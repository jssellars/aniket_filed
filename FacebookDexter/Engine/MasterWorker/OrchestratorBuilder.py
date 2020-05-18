import typing

from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from FacebookDexter.Infrastructure.PersistanceLayer.DexterMongoRepository import DexterMongoRepository
from FacebookDexter.Infrastructure.PersistanceLayer.DexterRecommendationsMongoRepository import \
    DexterRecommendationsMongoRepository


class OrchestratorBuilder:

    def __init__(self):
        self.business_owner_id = None
        self.ad_account_id = None
        self.level = None
        self.startup = None
        self.algorithm_type = None

        self._data_repository = None
        self._recommendations_repository = None
        self._journal_repository = None

    def set_business_owner_id(self, business_owner_id: typing.AnyStr = None):
        self.business_owner_id = business_owner_id
        return self

    def set_ad_account_id(self, ad_account_id: typing.AnyStr = None):
        self.ad_account_id = ad_account_id
        return self

    def set_level(self, level: LevelEnum = None):
        self.level = level
        return self

    def set_startup(self, startup: typing.Any = None):
        self.startup = startup
        return self

    def set_algorithm_type(self, algorithm_type):
        self.algorithm_type = algorithm_type
        return self

    def set_data_repository(self, repository: DexterMongoRepository = None):
        self._data_repository = repository
        return self

    def set_recommendations_repository(self, repository: DexterRecommendationsMongoRepository = None):
        self._recommendations_repository = repository
        return self

    def set_journal_repository(self, repository: DexterJournalMongoRepository = None):
        self._journal_repository = repository
        return self
