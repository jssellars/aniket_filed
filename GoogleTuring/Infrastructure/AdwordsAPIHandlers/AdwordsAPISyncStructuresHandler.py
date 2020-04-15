from datetime import datetime

from Core.Tools.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from Core.Tools.MongoRepository.MongoRepositoryBase import MongoRepositoryBase
from Core.Web.GoogleAdWordsAPI.AdWordsBaseClient import AdWordsBaseClient
from GoogleTuring.BackgroundTasks.Startup import startup
from GoogleTuring.BackgroundTasks.StructureSynchronizer import StructureSynchronizer


class AdwordsAPISyncStructuresHandler:

    @classmethod
    def handle(cls, request):
        refresh_token = request.refresh_token
        client = AdWordsBaseClient(config=startup.google_config, refresh_token=refresh_token)
        mongo_conn_handler = MongoConnectionHandler(startup.mongo_config)
        mongo_repository = MongoRepositoryBase(client=mongo_conn_handler.client, database_name=startup.mongo_config['googleAccountsDatabaseName'],
                                               collection_name=startup.mongo_config['accountsCollectionName'])

        account_info = list(set([(customer.google_id, customer.name) for customer in request.customers]))
        bo_google_id = request.google_id
        bo_email_address = request.email_address

        google_bo_document = {
            'business_owner_google_id': bo_google_id,
            'business_owner_email_address': bo_email_address,
            'refresh_token': refresh_token,
            'client_customer_ids': [{'google_id': google_id, 'name': name} for google_id, name in account_info],
            'last_update_time': datetime.now()
        }

        mongo_repository.add_one(google_bo_document)
        account_ids = list(map(lambda x: x[0], account_info))
        structure_synchronizer = StructureSynchronizer(business_owner_id=bo_google_id, account_ids=account_ids, adwords_client=client, mongo_config=startup.mongo_config)
        structure_synchronizer.synchronize_structures()
