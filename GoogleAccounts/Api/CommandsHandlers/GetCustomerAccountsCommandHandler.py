from Core.mongo_adapter import MongoOperator, MongoRepositoryBase
from GoogleAccounts.Api.startup import config


class GetCustomerAccountsCommandHandler:
    accounts_tree_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.google_accounts_database_name,
        collection_name=config.mongo.customers_collection_name,
    )

    @classmethod
    def handle(cls, google_business_owner_id):
        query = {"google_business_owner_id": {MongoOperator.EQUALS.value: google_business_owner_id}}
        feedback_docs = GetCustomerAccountsCommandHandler.accounts_tree_repository.get(query=query)
        return feedback_docs[0]["customers"]
