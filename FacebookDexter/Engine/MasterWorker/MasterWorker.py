import threading
import typing

from Core.Web.Security.Authorization import generate_technical_token, add_bearer_token
from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import AlgorithmsEnum
from FacebookDexter.Engine.MasterWorker.Orchestrator import Orchestrator
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from FacebookDexter.Infrastructure.PersistanceLayer.DexterMongoRepository import DexterMongoRepository
from FacebookDexter.Infrastructure.PersistanceLayer.DexterRecommendationsMongoRepository import \
    DexterRecommendationsMongoRepository


def start_algorithm_for_accounts_set(ad_account_ids: typing.List[typing.AnyStr] = None,
                                     business_owner_id: typing.AnyStr = None,
                                     startup: typing.Any = None,
                                     recommendations_repository: DexterRecommendationsMongoRepository = None,
                                     journal_repository: DexterJournalMongoRepository = None):
    data_repository = DexterMongoRepository(config=startup.mongo_config)
    orchestrator = (Orchestrator().
                    set_recommendations_repository(recommendations_repository).
                    set_journal_repository(journal_repository).
                    set_data_repository(data_repository))

    auth_token = add_bearer_token(token=generate_technical_token(startup))

    for ad_account_id in ad_account_ids:
        orchestrator.business_owner_id = business_owner_id
        orchestrator.ad_account_id = ad_account_id
        orchestrator.startup = startup

        (orchestrator.
            set_auth_token(auth_token=auth_token).
            orchestrate().
            update_remaining_null_dates())


def start_dexter_for_business_owner(business_owner: typing.AnyStr = None,
                                    startup: typing.Any = None,
                                    recommendations_repository: DexterRecommendationsMongoRepository = None,
                                    journal_repository: DexterJournalMongoRepository = None) -> typing.NoReturn:
    batch_size = business_owner.get_batch_size()
    number_of_account_ids = len(business_owner)

    for start in range(0, number_of_account_ids, batch_size):
        if start + batch_size < number_of_account_ids:
            child_thread = threading.Thread(target=start_algorithm_for_accounts_set,
                                            args=(business_owner.ad_account_ids[start:start + batch_size],
                                                  business_owner.business_owner_facebook_id,
                                                  startup,
                                                  recommendations_repository,
                                                  journal_repository))
            child_thread.start()

            #  Uncomment if you want to run in single thread
            # start_algorithm_for_accounts_set(business_owner.ad_account_ids[start:start + batch_size],
            #                                  business_owner.business_owner_facebook_id,
            #                                  startup,
            #                                  recommendations_repository,
            #                                  journal_repository)
        else:
            child_thread = threading.Thread(target=start_algorithm_for_accounts_set,
                                            args=(business_owner.ad_account_ids[start:],
                                                  business_owner.business_owner_facebook_id,
                                                  startup,
                                                  recommendations_repository,
                                                  journal_repository))
            child_thread.start()

            #  Uncomment if you want to run in single thread
            # start_algorithm_for_accounts_set(business_owner.ad_account_ids[start:],
            #                                  business_owner.business_owner_facebook_id,
            #                                  startup,
            #                                  recommendations_repository,
            #                                  journal_repository)
