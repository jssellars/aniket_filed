from datetime import datetime

from Core.Tools.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase
from Core.Web.GoogleAdWordsAPI.AdWordsAPI.AdWordsBaseClient import AdWordsBaseClient
from GoogleTuring.BackgroundTasks.Startup import startup
from GoogleTuring.BackgroundTasks.SyncJobs.Synchronizers.InsightsSynchronizer import InsightsSynchronizer
from GoogleTuring.BackgroundTasks.SyncJobs.Synchronizers.StructuresSynchronizer import StructuresSynchronizer
from GoogleTuring.Infrastructure.PersistenceLayer.GoogleBusinessOwnerMongoRepository import \
    GoogleBusinessOwnerMongoRepository


def get_ad_accounts_details(mongo_conn_handler, logger=None):
    mongo_repository = GoogleBusinessOwnerMongoRepository(client=mongo_conn_handler.client,
                                                          database_name=startup.mongo_config[
                                                              'google_accounts_database_name'],
                                                          collection_name=startup.mongo_config[
                                                              'accounts_collection_name'],
                                                          logger=logger)

    result = mongo_repository.get_all_active_google_accounts()
    return result


def set_update_time(ad_account_id, mongo_conn_handler, logger=None):
    mongo_repository = MongoRepositoryBase(client=mongo_conn_handler.client,
                                           database_name=startup.mongo_config['google_accounts_database_name'],
                                           collection_name=startup.mongo_config['accounts_collection_name'],
                                           logger=logger)

    query_filter = {
        "client_customer_id": {MongoOperator.EQUALS.value: ad_account_id}
    }
    query = {
        MongoOperator.SET.value: {
            "last_updated_time": datetime.now()
        }
    }
    mongo_repository.update_one(query_filter=query_filter, query=query)


def daily_sync_job(logger):
    mongo_conn_handler = MongoConnectionHandler(startup.mongo_config)
    ad_accounts_to_sync = get_ad_accounts_details(mongo_conn_handler, logger=logger)

    for ad_account in ad_accounts_to_sync:
        refresh_token = ad_account['refresh_token']
        bo_google_id = ad_account['business_owner_google_id']
        account_id = ad_account['client_customer_id']['google_id']
        last_update_time = ad_account['last_update_time']
        client = AdWordsBaseClient(config=startup.google_config, refresh_token=refresh_token, logger=logger)
        structure_synchronizer = StructuresSynchronizer(business_owner_id=bo_google_id, account_id=account_id,
                                                        adwords_client=client,
                                                        mongo_config=startup.mongo_config,
                                                        mongo_conn_handler=mongo_conn_handler,
                                                        logger=logger)
        structure_synchronizer.synchronize()
        insight_synchronizer = InsightsSynchronizer(business_owner_id=bo_google_id, account_id=account_id,
                                                    adwords_client=client,
                                                    mongo_config=startup.mongo_config,
                                                    last_update_time=last_update_time,
                                                    mongo_conn_handler=mongo_conn_handler,
                                                    logger=logger)
        insight_synchronizer.synchronize()
        set_update_time(account_id, mongo_conn_handler, logger=logger)
