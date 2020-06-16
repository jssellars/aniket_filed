import json

from GoogleDexter.Engine.MasterWorker import MasterWorker
from GoogleDexter.Infrastructure.IntegrationEvents.GoogleTuringDataSyncCompletedEvent import \
    GoogleTuringDataSyncCompletedEvent
from GoogleDexter.Infrastructure.IntegrationEvents.GoogleTuringDataSyncCompletedEventMapping import \
    GoogleTuringDataSyncCompletedEventMapping
from GoogleDexter.Infrastructure.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from GoogleDexter.Infrastructure.PersistanceLayer.DexterMongoRepository import DexterMongoRepository
from GoogleDexter.Infrastructure.PersistanceLayer.DexterRecommendationsMongoRepository import \
    DexterRecommendationsMongoRepository


class GoogleTuringDataSyncCompletedEventHandler:
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

        mapper = GoogleTuringDataSyncCompletedEventMapping(target=GoogleTuringDataSyncCompletedEvent)
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
