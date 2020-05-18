import json

from FacebookDexter.Engine.MasterWorker import MasterWorker
from FacebookDexter.Infrastructure.IntegrationEvents.FacebookTuringDataSyncCompletedEvent import \
    FacebookTuringDataSyncCompletedEvent
from FacebookDexter.Infrastructure.IntegrationEvents.FacebookTuringDataSyncCompletedEventMapping import \
    FacebookTuringDataSyncCompletedEventMapping
from FacebookDexter.Infrastructure.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from FacebookDexter.Infrastructure.PersistanceLayer.DexterMongoRepository import DexterMongoRepository
from FacebookDexter.Infrastructure.PersistanceLayer.DexterRecommendationsMongoRepository import \
    DexterRecommendationsMongoRepository


class FacebookTuringDataSyncCompletedEventHandler:
    __startup = None
    __data_repository = None
    __recommendations_repository = None
    __journal_repository = None
    __journal_helper_repository = None

    @classmethod
    def set_startup(cls, startup):
        cls.__startup = startup
        return cls

    @classmethod
    def set_data_repository(cls, repository: DexterMongoRepository = None):
        cls.__data_repository = repository
        return cls

    @classmethod
    def set_recommendations_repository(cls, repository: DexterRecommendationsMongoRepository = None):
        cls.__recommendations_repository = repository
        return cls

    @classmethod
    def set_journal_repository(cls, repository: DexterJournalMongoRepository = None):
        cls.__journal_repository = repository
        return cls

    @classmethod
    def handle(cls, body):
        body = json.loads(body)

        mapper = FacebookTuringDataSyncCompletedEventMapping(target=FacebookTuringDataSyncCompletedEvent)
        business_owners = mapper.load(body.get("business_owners", []), many=True)

        for business_owner in business_owners:
            # business_owner_thread = threading.Thread(target=MasterWorker.start_dexter_for_business_owner,
            #                                          args=(business_owner,
            #                                                cls.__startup,
            #                                                cls.__data_repository,
            #                                                cls.__recommendations_repository,
            #                                                cls.__journal_repository))
            # business_owner_thread.start()
            MasterWorker.start_dexter_for_business_owner(business_owner,
                                                         cls.__startup,
                                                         cls.__data_repository,
                                                         cls.__recommendations_repository,
                                                         cls.__journal_repository)
