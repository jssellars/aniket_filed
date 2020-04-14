import threading

from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import AlgorithmsEnum

from FacebookDexter.Engine.MasterWorker.Orchestrator import Orchestrator
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.BackgroundTasks.Startup import startup

def start_algorithm_for_accounts_set(ad_account_ids, business_owner_id):

    orchestrator = Orchestrator()

    for ad_account_id in ad_account_ids:
        for algorithm_type in AlgorithmsEnum:
            for level in LevelEnum:
                orchestrator.__business_owner_id = business_owner_id
                orchestrator.__ad_account_id = ad_account_id
                orchestrator.__algorithm_type = algorithm_type
                orchestrator.__level = level
                orchestrator.__startup = startup

                orchestrator.orchestrate()

        orchestrator.update_remaining_null_dates()


def start_dexter_for_business_owner(business_owner):
    batch_size = business_owner.get_batch_size()
    number_of_account_ids = business_owner.get_number_of_account_ids()

    for start in range(0, number_of_account_ids, batch_size):
        if start + batch_size < number_of_account_ids:
            child_thread = threading.Thread(target=start_algorithm_for_accounts_set, args=(business_owner.ad_account_ids[start:start + batch_size],
                                                                                           business_owner.business_owner_id))
            child_thread.start()
        else:
            child_thread = threading.Thread(target=start_algorithm_for_accounts_set, args=(business_owner.ad_account_ids[start:],
                                                                                           business_owner.business_owner_id))
            child_thread.start()
