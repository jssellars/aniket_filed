from datetime import datetime, timedelta

from Core.Tools.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase
from Core.Web.GoogleAdWordsAPI.AdWordsBaseClient import AdWordsBaseClient
from GoogleTuring.BackgroundTasks.Startup import startup
from GoogleTuring.BackgroundTasks.StructureSynchronizer import StructureSynchronizer


def get_business_owner_details():
    mongo_conn_handler = MongoConnectionHandler(startup.mongo_config)
    mongo_repository = MongoRepositoryBase(client=mongo_conn_handler.client, database_name=startup.mongo_config['googleAccountsDatabaseName'],
                                           collection_name=startup.mongo_config['accountsCollectionName'])

    business_owners_to_sync = mongo_repository.get_last_updated(datetime.now() - timedelta(days=1))
    return business_owners_to_sync


def set_update_time(business_owner_id):
    mongo_conn_handler = MongoConnectionHandler(startup.mongo_config)
    mongo_repository = MongoRepositoryBase(client=mongo_conn_handler.client, database_name=startup.mongo_config['googleAccountsDatabaseName'],
                                           collection_name=startup.mongo_config['accountsCollectionName'])

    query_filter = {
        "business_owner_google_id": {MongoOperator.EQUALS.value: business_owner_id['business_owner_google_id']}
    }
    query = {
        MongoOperator.SET.value: {
            "last_updated_time": datetime.now()
        }
    }
    mongo_repository.update_one(query_filter=query_filter, query=query)


def daily_sync_job():
    print('[Structure BT] Daily sync started')
    bo_to_sync = get_business_owner_details()

    for bo in bo_to_sync:
        refresh_token = bo['refresh_token']
        bo_google_id = bo['business_owner_google_id']
        account_ids = [customer['google_id'] for customer in bo['client_customer_ids']]
        client = AdWordsBaseClient(config=startup.google_config, refresh_token=refresh_token)
        structure_synchronizer = StructureSynchronizer(business_owner_id=bo_google_id, account_ids=account_ids, adwords_client=client, mongo_config=startup.mongo_config)
        structure_synchronizer.synchronize_structures()
        set_update_time(bo)
