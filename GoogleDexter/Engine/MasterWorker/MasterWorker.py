import typing

from GoogleDexter.Engine.Algorithms.AlgorithmsEnum import AlgorithmsEnum
from GoogleDexter.Engine.MasterWorker.Orchestrator import Orchestrator
from GoogleDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from GoogleDexter.Infrastructure.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from GoogleDexter.Infrastructure.PersistanceLayer.DexterMongoRepository import DexterMongoRepository
from GoogleDexter.Infrastructure.PersistanceLayer.DexterRecommendationsMongoRepository import \
    DexterRecommendationsMongoRepository


def start_algorithm_for_accounts_set(ad_account_ids: typing.List[typing.AnyStr] = None,
                                     business_owner_id: typing.AnyStr = None,
                                     startup: typing.Any = None,
                                     data_repository: DexterMongoRepository = None,
                                     recommendations_repository: DexterRecommendationsMongoRepository = None,
                                     journal_repository: DexterJournalMongoRepository = None):
    orchestrator = (Orchestrator().
                    set_data_repository(data_repository).
                    set_recommendations_repository(recommendations_repository).
                    set_journal_repository(journal_repository))

    levels = [LevelEnum.AD, LevelEnum.CAMPAIGN, LevelEnum.ADGROUP]
    generator = ((ad_account_id, algorithm_type, level)
                 for ad_account_id in ad_account_ids
                 for algorithm_type in AlgorithmsEnum
                 for level in levels)

    for ad_account_id, algorithm_type, level in generator:
        orchestrator.business_owner_id = business_owner_id
        orchestrator.ad_account_id = ad_account_id
        orchestrator.algorithm_type = algorithm_type
        orchestrator.level = level
        orchestrator.startup = startup

        orchestrator.orchestrate()
        orchestrator.update_remaining_null_dates()


def start_dexter_for_business_owner(business_owner: typing.AnyStr = None,
                                    startup: typing.Any = None,
                                    data_repository: DexterMongoRepository = None,
                                    recommendations_repository: DexterRecommendationsMongoRepository = None,
                                    journal_repository: DexterJournalMongoRepository = None) -> typing.NoReturn:
    batch_size = business_owner.get_batch_size()
    number_of_account_ids = len(business_owner)

    for start in range(0, number_of_account_ids, batch_size):
        if start + batch_size < number_of_account_ids:
            # child_thread = threading.Thread(target=start_algorithm_for_accounts_set, args=(business_owner.ad_account_ids[start:start + batch_size],
            #                                                                                business_owner.business_owner_google_id,
            #                                                                                startup,
            #                                                                                data_repository,
            #                                                                                recommendations_repository,
            #                                                                                journal_repository))
            # child_thread.start()
            start_algorithm_for_accounts_set(business_owner.ad_account_ids[start:start + batch_size],
                                             business_owner.business_owner_google_id,
                                             startup,
                                             data_repository,
                                             recommendations_repository,
                                             journal_repository)
        else:
            # child_thread = threading.Thread(target=start_algorithm_for_accounts_set, args=(business_owner.ad_account_ids[start:],
            #                                                                                business_owner.business_owner_google_id,
            #                                                                                startup,
            #                                                                                data_repository,
            #                                                                                recommendations_repository,
            #                                                                                journal_repository))
            # child_thread.start()
            start_algorithm_for_accounts_set(business_owner.ad_account_ids[start:],
                                             business_owner.business_owner_google_id,
                                             startup,
                                             data_repository,
                                             recommendations_repository,
                                             journal_repository)
