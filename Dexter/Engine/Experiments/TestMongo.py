from Packages.MongoRepository.MongoRepositoryBase import MongoRepositoryBase
from Packages.MongoRepository.MongoConnectionHandler import MongoConnectionHandler
from Startup import startup
from Packages.Tools.ObjectManipulators import extract_class_attributes_values
from Algorithms.Models.Types import TypesWrapper

mongo_connection_config = MongoConnectionHandler(mongo_config=startup.mongoConfig)
mongo_client = mongo_connection_config.client

mongo_repository_structures = MongoRepositoryBase(client=mongo_client, database_name=startup.mongoConfig.structuresDatabaseName)
all_structures_collections = mongo_repository_structures.get_all_collections()


# get all collections from insights db
mongo_repository_insights = MongoRepositoryBase(client=mongo_client, database_name=startup.mongoConfig.insightsDatabaseName)
all_insights_collections = mongo_repository_insights.get_all_collections()

# for each collection, get structure ids
level_to_ids = {}

for structures_collection in all_structures_collections:
    mongo_repository_structures.collection = structures_collection
    level_to_ids[structures_collection] = mongo_repository_structures.get_distinct_by_key(structures_collection + '_id')
    if None in level_to_ids[structures_collection]:
        level_to_ids[structures_collection].remove(None)

for insights_collection in all_insights_collections:
    mongo_repository_insights.collection = insights_collection
    level = insights_collection.split('-')[0]
    breakdown = insights_collection.split('-')[1]
    action_breakdown = insights_collection.split('-')[2]

    combination = TypesWrapper.OptimizationTuple(level, breakdown, action_breakdown)
    ids = level_to_ids[level]

    for id in ids:
        insights = mongo_repository_insights.get_all_by_key(level + "_id", [id])
        if insights:
            print('ceva')

# preprocess structure insights
from Models.TuringFields.Field import TuringFieldsMetadata

print(TuringFieldsMetadata.__dict__.keys())
print(getattr(TuringFieldsMetadata, 'all_cpc'))
mapped_insights = [{field.dexter_key: entry[field.turing_key] for field in extract_class_attributes_values(TuringFieldsMetadata)} for entry in insights]

# run Dexter

# mongo_repository.collection = ""
# mongo_repository.add_many()
