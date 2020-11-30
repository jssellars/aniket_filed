import typing

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.MasterWorkerBase import MasterWorkerBase
from Core.Dexter.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from Core.Dexter.PersistanceLayer.DexterRecommendationsMongoRepository import DexterRecommendationsMongoRepository
from Core.Web.Security.Authorization import add_bearer_token, generate_technical_token
from GoogleDexter.Engine.MasterWorker.GoogleOrchestratorFactory import GoogleOrchestratorFactory
from GoogleDexter.Engine.MasterWorker.GoogleStrategyEnum import GoogleStrategyEnum
from GoogleDexter.Infrastructure.PersistanceLayer.GoogleDexterMongoRepository import GoogleDexterMongoRepository


class GoogleMasterWorker(MasterWorkerBase):

    def __init__(self):
        super().__init__()

    def start_algorithm_for_accounts_set(self,
                                         ad_account_ids: typing.List[typing.AnyStr] = None,
                                         business_owner_id: typing.AnyStr = None,
                                         startup: typing.Any = None,
                                         logger: typing.Any = None,
                                         recommendations_repository: DexterRecommendationsMongoRepository = None,
                                         journal_repository: DexterJournalMongoRepository = None,
                                         channel: ChannelEnum = None):

        # auth_token = add_bearer_token(token=generate_technical_token(startup.technical_token_manager))

        orchestrator = GoogleOrchestratorFactory.get(GoogleStrategyEnum.DEFAULT)
        (orchestrator.set_recommendations_repository(recommendations_repository).
         set_journal_repository(journal_repository).
         set_data_repository(GoogleDexterMongoRepository(config=startup.mongo_config)).
         set_business_owner_id(business_owner_id).
         set_startup(startup))

        for time_interval in startup.dexter_config.time_intervals:
            for ad_account_id in ad_account_ids:
                orchestrator.set_ad_account_id(ad_account_id)
                search_query = orchestrator.orchestrate(time_interval)
                if search_query:
                    orchestrator.run_algorithm(search_query, time_interval, startup.mongo_config)
                orchestrator.update_remaining_null_dates()
