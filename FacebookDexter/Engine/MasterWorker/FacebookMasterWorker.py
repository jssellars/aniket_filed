import typing

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.MasterWorkerBase import MasterWorkerBase
from Core.Dexter.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from Core.Dexter.PersistanceLayer.DexterRecommendationsMongoRepository import DexterRecommendationsMongoRepository
from Core.Web.Security.Authorization import add_bearer_token, generate_technical_token
from FacebookDexter.BackgroundTasks.startup import fixtures
from FacebookDexter.Engine.MasterWorker.FacebookOrchestratorFactory import FacebookOrchestratorFactory
from FacebookDexter.Engine.MasterWorker.FacebookStrategyEnum import FacebookStrategyEnum


class FacebookMasterWorker(MasterWorkerBase):

    def __init__(self):
        super().__init__()

    def start_algorithm_for_accounts_set(self,
                                         ad_account_ids: typing.List[typing.AnyStr] = None,
                                         business_owner_id: typing.AnyStr = None,
                                         config: typing.Any = None,
                                         logger: typing.Any = None,
                                         recommendations_repository: DexterRecommendationsMongoRepository = None,
                                         journal_repository: DexterJournalMongoRepository = None,
                                         channel: ChannelEnum = None):

        auth_token = add_bearer_token(token=generate_technical_token(fixtures.technical_token_manager))

        orchestrator = FacebookOrchestratorFactory.get(FacebookStrategyEnum.SINGLE_METRIC)
        (orchestrator.set_recommendations_repository(recommendations_repository).
         set_journal_repository(journal_repository).
         set_auth_token(auth_token=auth_token).
         set_business_owner_id(business_owner_id).
         set_config(config))

        for time_interval in config.dexter.time_intervals:
            for ad_account_id in ad_account_ids:
                orchestrator.set_ad_account_id(ad_account_id)
                search_query = orchestrator.orchestrate(time_interval)
                if search_query:
                    orchestrator.run_algorithm(search_query, time_interval, config.mongo)

                orchestrator.update_remaining_null_dates()

        # TODO: this should be tested properly, it might not work as expected
        # still_running = True
        # algorithm_query = DexterJournalMongoRepositoryHelper.get_existing_pending_jobs_for_account(orchestrator.algorithm_type)

        # while still_running:
        #     pending_jobs = journal_repository.get_all_by_query(algorithm_query)
        #     if not pending_jobs:
        #         still_running = False
        #     else:
        #         for pending_job in pending_jobs:
        #             (orchestrator.
        #              set_business_owner_id(pending_job['business_owner_id']).
        #              set_ad_account_id(pending_job['ad_account_id']))
        #             time_interval = pending_job['time_interval']
        #             search_query = orchestrator.orchestrate(time_interval)
        #             if search_query:
        #                 orchestrator.run_algorithm(search_query, time_interval, config.mongo)
