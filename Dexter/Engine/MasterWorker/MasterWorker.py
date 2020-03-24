from Algorithms.Dexter_Fuzzy_Inference.Tools import MongoPrerequisites
from Algorithms.Tools.Columns import AlgorithmName
from MasterWorker.Orchestrator import Orchestrator
import threading

def start_algorithm_for_accounts_set(ad_account_ids, business_owner_id, channel):
    mongo_recommender = MongoPrerequisites.get_mongo_recommender()
    mongo_journalizer = MongoPrerequisites.get_mongo_journalizer()

    orchestrator = Orchestrator()

    all_insights_collections, mongo_repository_insights = MongoPrerequisites.get_data_from_mongo()
    orchestrator.all_insights_collections = all_insights_collections

    for ad_account_id in ad_account_ids:
        for algorithm_type in AlgorithmName:

            orchestrator.business_owner_id = business_owner_id
            orchestrator.ad_account_id = ad_account_id
            orchestrator.algorithm_type = algorithm_type
            orchestrator.channel = channel

            orchestrator.orchestrate(mongo_recommender=mongo_recommender,
                                     mongo_journalizer=mongo_journalizer,
                                     mongo_repository_insights=mongo_repository_insights)

        # TODO: check on this if its okay. it may be that I am updating without thinking
        orchestrator.update_remaining_null_dates(mongo_journalizer)


def start_dexter_for_business_owner(business_owner, channel):
    batch_size = business_owner.get_batch_size()
    number_of_account_ids = business_owner.get_number_of_account_ids()

    for start in range(0, number_of_account_ids, batch_size):
        if start + batch_size < number_of_account_ids:
            child_thread = threading.Thread(target=start_algorithm_for_accounts_set, args=(business_owner.ad_account_ids[start:start + batch_size],
                                                                                           business_owner.business_owner_id,
                                                                                           channel))
            child_thread.start()
            # start_algorithm_for_accounts_set(business_owner.ad_account_ids[start:start + batch_size - 1], business_owner.business_owner_id, channel)
        else:
            child_thread = threading.Thread(target=start_algorithm_for_accounts_set, args=(business_owner.ad_account_ids[start:],
                                                                                           business_owner.business_owner_id,
                                                                                           channel))
            child_thread.start()
            # start_algorithm_for_accounts_set(business_owner.ad_account_ids[start:], business_owner.business_owner_id, channel)
