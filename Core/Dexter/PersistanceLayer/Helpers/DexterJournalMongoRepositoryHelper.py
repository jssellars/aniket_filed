from datetime import datetime

from Core.Dexter.Infrastructure.Domain.DexterJournalEnums import RunStatusDexterEngineJournal


class DexterJournalMongoRepositoryHelper:

    @staticmethod
    def get_search_in_progress_query(ad_account_id, business_owner_id, time_interval, algorithm_type):
        return {
            'ad_account_id': ad_account_id,
            'business_owner_id': business_owner_id,
            'run_status': RunStatusDexterEngineJournal.IN_PROGRESS.value,
            'time_interval': time_interval,
            'algorithm_type': algorithm_type.value
        }

    @staticmethod
    def get_search_pending_query(ad_account_id, business_owner_id, time_interval, algorithm_type):
        return {
            'ad_account_id': ad_account_id,
            'business_owner_id': business_owner_id,
            'run_status': RunStatusDexterEngineJournal.PENDING.value,
            'time_interval': time_interval,
            'algorithm_type': algorithm_type.value
        }

    @staticmethod
    def get_update_query_in_progress():
        return {
            '$set': {
                'start_timestamp': datetime.now(),
                'run_status': RunStatusDexterEngineJournal.IN_PROGRESS.value
            }
        }

    @staticmethod
    def get_update_query_start_date_only():
        return {
            '$set': {
                'start_timestamp': datetime.now()
            }
        }

    @staticmethod
    def get_update_query_for_null_entries():
        return {
            '$set': {
                'end_timestamp': datetime.now()
            }
        }

    @staticmethod
    def get_update_query_completed():
        return {
            '$set': {
                'end_timestamp': datetime.now(),
                'run_status': RunStatusDexterEngineJournal.COMPLETED.value
            }
        }

    @staticmethod
    def get_update_query_failed():
        return {
            '$set': {
                'end_timestamp': datetime.now(),
                'run_status': RunStatusDexterEngineJournal.FAILED.value
            }
        }

    @staticmethod
    def get_search_for_other_instances_query(business_owner_id, ad_account_id, time_interval, algorithm_type):
        return {
            "business_owner_id": business_owner_id,
            "ad_account_id": ad_account_id,
            'time_interval': time_interval,
            'algorithm_type': algorithm_type.value
        }

    @staticmethod
    def get_sort_descending_by_start_date_query():
        return [('start_date', -1)]

    @staticmethod
    def get_search_for_null_end_date(business_owner_id, ad_account_id, algorithm_type):
        return {
            "business_owner_id": business_owner_id,
            "ad_account_id": ad_account_id,
            'algorithm_type': algorithm_type.value
        }

    @staticmethod
    def get_existing_pending_jobs_for_account(algorithm_type):
        return {
            'algorithm_type': algorithm_type.value,
            'run_status': RunStatusDexterEngineJournal.PENDING.value
        }
