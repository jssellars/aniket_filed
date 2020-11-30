import json

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from Core.Dexter.PersistanceLayer.DexterRecommendationsMongoRepository import DexterRecommendationsMongoRepository
from FacebookDexter.Engine.MasterWorker.FacebookMasterWorker import FacebookMasterWorker
from FacebookDexter.Infrastructure.IntegrationEvents.FacebookTuringDataSyncCompletedEvent import \
    FacebookTuringDataSyncCompletedEvent
from FacebookDexter.Infrastructure.IntegrationEvents.FacebookTuringDataSyncCompletedEventMapping import \
    FacebookTuringDataSyncCompletedEventMapping
from FacebookDexter.Infrastructure.PersistanceLayer.FacebookDexterMongoRepository import FacebookDexterMongoRepository


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
    def set_data_repository(cls, repository: FacebookDexterMongoRepository = None):
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
        fb_mw = FacebookMasterWorker()
        for business_owner in business_owners:
            fb_mw.start_dexter_for_business_owner(business_owner.business_owner_facebook_id,
                                                  business_owner.ad_account_ids,
                                                  cls.__startup,
                                                  cls.__logger,
                                                  cls.__recommendations_repository,
                                                  cls.__journal_repository,
                                                  channel=ChannelEnum.FACEBOOK)
