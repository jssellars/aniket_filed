from Packages.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from Packages.MongoRepository.MongoRepositoryBase import MongoRepositoryBase
from Packages.MongoRepository.MongoRepositoryJournalizer import MongoRepositoryJournalizer
from Packages.MongoRepository.MongoRepositoryRecommender import MongoRepositoryRecommender
from Startup import startup


# TODO: take another look at this, needs refactoring, i have no idea hwow to do it
def get_mongo_recommender():
    mongo_recommender_connection_config = MongoConnectionHandler(mongo_config=startup.mongoConfig)
    mongo_client_recommender = mongo_recommender_connection_config.client

    mongo_recommender = MongoRepositoryRecommender(client=mongo_client_recommender, database_name=startup.mongoConfig.recommendationDatabaseName)
    mongo_recommender.collection = startup.mongoConfig.recommendationCollectionName

    return mongo_recommender


def get_data_from_mongo():
    mongo_repository_insights_connection_config = MongoConnectionHandler(mongo_config=startup.mongoConfig)
    mongo_client_repository_insights = mongo_repository_insights_connection_config.client

    mongo_repository_insights = MongoRepositoryBase(client=mongo_client_repository_insights, database_name=startup.mongoConfig.insightsDatabaseName)
    # TODO: decide how to get data
    all_insights_collections = mongo_repository_insights.get_all_collections()

    return all_insights_collections, mongo_repository_insights


def get_mongo_journalizer():
    mongo_journalizer_connection_config = MongoConnectionHandler(mongo_config=startup.mongoConfig)
    mongo_journalizer_client = mongo_journalizer_connection_config.client

    mongo_journalizer = MongoRepositoryJournalizer(client=mongo_journalizer_client, database_name=startup.mongoConfig.dexterJournalDatabaseName)
    mongo_journalizer.collection = startup.mongoConfig.dexterJournalCollectionName

    return mongo_journalizer
