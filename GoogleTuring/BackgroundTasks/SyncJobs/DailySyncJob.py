from datetime import datetime

from Core.mongo_adapter import MongoRepositoryBase, MongoOperator
from Core.Web.GoogleAdWordsAPI.AdWordsAPI.AdWordsBaseClient import AdWordsBaseClient
from GoogleTuring.BackgroundTasks.startup import config, fixtures
from GoogleTuring.BackgroundTasks.SyncJobs.Synchronizers.InsightsSynchronizer import InsightsSynchronizer
from GoogleTuring.BackgroundTasks.SyncJobs.Synchronizers.StructuresSynchronizer import StructuresSynchronizer
from GoogleTuring.Infrastructure.PersistenceLayer.GoogleBusinessOwnerMongoRepository import \
    GoogleBusinessOwnerMongoRepository


def get_ad_accounts_details(mongo_adapter):
    mongo_repository = GoogleBusinessOwnerMongoRepository(client=mongo_adapter.client,
                                                          database_name=config.mongo.google_accounts_database_name,
                                                          collection_name=config.mongo.accounts_collection_name)

    result = mongo_repository.get_all_active_google_accounts()
    return result


def set_update_time(ad_account_id, mongo_adapter):
    mongo_repository = MongoRepositoryBase(client=mongo_adapter.client,
                                           database_name=config.mongo.google_accounts_database_name,
                                           collection_name=config.mongo.accounts_collection_name)

    query_filter = {
        "client_customer_id": {MongoOperator.EQUALS.value: ad_account_id}
    }
    query = {
        MongoOperator.SET.value: {
            "last_updated_time": datetime.now()
        }
    }
    mongo_repository.update_one(query_filter=query_filter, query=query)


def daily_sync_job():
    mongo_adapter = fixtures.mongo_adapter
    ad_accounts_to_sync = get_ad_accounts_details(mongo_adapter)

    for ad_account in ad_accounts_to_sync:
        refresh_token = ad_account['refresh_token']
        bo_google_id = ad_account['business_owner_google_id']
        account_id = ad_account['client_customer_id']['google_id']
        last_update_time = ad_account['last_update_time']
        client = AdWordsBaseClient(config=config.google, refresh_token=refresh_token)
        structure_synchronizer = StructuresSynchronizer(business_owner_id=bo_google_id, account_id=account_id,
                                                        adwords_client=client,
                                                        mongo_config=config.mongo,
                                                        mongo_adapter=mongo_adapter)
        structure_synchronizer.synchronize()
        insight_synchronizer = InsightsSynchronizer(business_owner_id=bo_google_id, account_id=account_id,
                                                    adwords_client=client,
                                                    mongo_config=config.mongo,
                                                    last_update_time=last_update_time,
                                                    mongo_adapter=mongo_adapter)
        insight_synchronizer.synchronize()
        set_update_time(account_id, mongo_adapter)
