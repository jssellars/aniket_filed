from datetime import datetime

from Core.Tools.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from Core.Tools.MongoRepository.MongoOperator import MongoOperator
from Core.Web.GoogleAdWordsAPI.AdWordsAPI.AdWordsBaseClient import AdWordsBaseClient
from GoogleTuring.BackgroundTasks.Startup import startup
from GoogleTuring.BackgroundTasks.SyncJobs.Synchronizers.InsightsSynchronizer import InsightsSynchronizer
from GoogleTuring.BackgroundTasks.SyncJobs.Synchronizers.StructuresSynchronizer import StructuresSynchronizer
from GoogleTuring.Infrastructure.Domain.Enums.GoogleAccountStatus import GoogleAccountStatus
from GoogleTuring.Infrastructure.PersistenceLayer.GoogleBusinessOwnerMongoRepository import \
    GoogleBusinessOwnerMongoRepository
from GoogleTuring.Infrastructure.PersistenceLayer.GoogleTuringStructuresMongoRepository import \
    GoogleTuringStructuresMongoRepository


class AdWordsAPIDataSyncHandler:

    @classmethod
    def handle(cls, request):
        refresh_token = request.refresh_token
        client = AdWordsBaseClient(config=startup.google_config, refresh_token=refresh_token)
        mongo_conn_handler = MongoConnectionHandler(startup.mongo_config)
        mongo_repository = GoogleBusinessOwnerMongoRepository(client=mongo_conn_handler.client,
                                                              database_name=startup.mongo_config[
                                                                  'google_accounts_database_name'],
                                                              collection_name=startup.mongo_config[
                                                                  'accounts_collection_name'])

        account_info = list(set([(str(customer.google_id), customer.name) for customer in request.customers]))
        bo_google_id = request.google_id
        bo_email_address = request.email_address

        google_account_documents = [{
            'business_owner_google_id': bo_google_id,
            'business_owner_email_address': bo_email_address,
            'refresh_token': refresh_token,
            'client_customer_id': {'google_id': google_id, 'name': name},
            'status': GoogleAccountStatus.ACTIVE.value
        } for google_id, name in account_info]

        account_ids = list(map(lambda x: x[0], account_info))
        active_google_accounts = mongo_repository.get_active_google_accounts(business_owner_id=bo_google_id)

        removed_customer_ids = []
        google_id_to_last_update_time = {}

        if active_google_accounts:
            client_customer_ids = [google_account['client_customer_id']['google_id'] for google_account in
                                   active_google_accounts]
            google_id_to_last_update_time = {
                google_account['client_customer_id']['google_id']: google_account['last_update_time'] for
                google_account in
                active_google_accounts}
            removed_customer_ids = list(set(client_customer_ids) - set(account_ids))
            mongo_repository.change_status_many(ids=removed_customer_ids, new_status=GoogleAccountStatus.REMOVED.value,
                                                id_key="client_customer_id.google_id")

        mongo_structures_repository = GoogleTuringStructuresMongoRepository(client=mongo_conn_handler.client,
                                                                            database_name=startup.mongo_config[
                                                                                'google_structures_database_name'])
        mongo_structures_repository.update_removed_structures(removed_customer_ids)

        for i, account_id in enumerate(account_ids):
            structures_synchronizer = StructuresSynchronizer(business_owner_id=bo_google_id, account_id=account_id,
                                                             adwords_client=client, mongo_config=startup.mongo_config,
                                                             mongo_conn_handler=mongo_conn_handler)
            structures_synchronizer.synchronize()
            last_update_time = google_id_to_last_update_time.get(account_id, None)
            insights_synchronizer = InsightsSynchronizer(business_owner_id=bo_google_id, account_id=account_id,
                                                         adwords_client=client, mongo_config=startup.mongo_config,
                                                         last_update_time=last_update_time,
                                                         mongo_conn_handler=mongo_conn_handler)
            insights_synchronizer.synchronize()

            google_account_doc = google_account_documents[i]
            google_account_doc['last_update_time'] = datetime.now()
            if last_update_time:
                query_filter = {
                    "client_customer_id.google_id": {MongoOperator.EQUALS.value: account_id}
                }
                query = {
                    MongoOperator.SET.value: google_account_doc
                }
                mongo_repository.update_one(query_filter=query_filter, query=query)
            else:
                mongo_repository.add_one(google_account_doc)
