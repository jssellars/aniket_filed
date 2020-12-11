import json

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from Core.Dexter.PersistanceLayer.DexterRecommendationsMongoRepository import DexterRecommendationsMongoRepository
from GoogleDexter.Engine.MasterWorker.GoogleMasterWorker import GoogleMasterWorker
from GoogleDexter.Infrastructure.IntegrationEvents.GoogleTuringDataSyncCompletedEvent import \
    GoogleTuringDataSyncCompletedEvent
from GoogleDexter.Infrastructure.IntegrationEvents.GoogleTuringDataSyncCompletedEventMapping import \
    GoogleTuringDataSyncCompletedEventMapping
from GoogleDexter.Infrastructure.PersistanceLayer.GoogleDexterMongoRepository import GoogleDexterMongoRepository


class GoogleTuringDataSyncCompletedEventHandler:
    _config = None
    __data_repository = None
    __recommendations_repository = None
    __journal_repository = None
    __journal_helper_repository = None

    @classmethod
    def set_config(cls, config):
        cls._config = config
        return cls

    @classmethod
    def set_data_repository(cls, repository: GoogleDexterMongoRepository = None):
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
        google_mw = GoogleMasterWorker()
        for business_owner in business_owners:
            # business_owner_thread = threading.Thread(target=MasterWorker.start_dexter_for_business_owner,
            #                                          args=(business_owner,
            #                                                cls._config,
            #                                                cls.__data_repository,
            #                                                cls.__recommendations_repository,
            #                                                cls.__journal_repository))
            # business_owner_thread.start()
            google_mw.start_dexter_for_business_owner(business_owner.business_owner_google_id,
                                                      business_owner.ad_account_ids,
                                                      cls._config,
                                                      cls.__recommendations_repository,
                                                      cls.__journal_repository,
                                                      ChannelEnum.GOOGLE)
