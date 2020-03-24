import logging
from copy import deepcopy

import pymongo
from Config.DbData import InternalTables as TableData

from Algorithms.Models.Types import TypesWrapper as Tw
from Algorithms.Tools import ColumnsEnum, Columns
from Algorithms.Tools.TimeInterval import TimeInterval


class MongoMediator:
    """Wraps the mediator in a singleton package to be used with standard object instantiation syntax"""
    __instance = None

    def __init__(self):
        if not MongoMediator.has_instance():
            MongoMediator.__instance = MongoInstance()

    @staticmethod
    def has_instance():
        boolean_value = MongoMediator.__instance != None
        return boolean_value

    # Not used. Could be extended to a nice approach fetching all public methods of the instance and adding them ( as still to the instance bound methods ) to the methods of the singleton wrapper
    def __get_instance_methods(self):
        instance = MongoMediator.__instance
        instance_methods = [method_name for method_name in dir(instance)
                           if callable(getattr(instance, method_name))]

        class_prefix = instance.__class__.__name__
        for instance_method in instance_methods:
            if class_prefix in instance_method:
                print(instance_method)

    def store_optimization_types(self, types):
        return MongoMediator.__instance.store_optimization_types(types)

    def store_expanded_types(self, expanded_types):
        return MongoMediator.__instance.store_expanded_types(expanded_types)

    def store_insights_data(self, data, optimization_tuple: Tw.OptimizationTuple):
        return MongoMediator.__instance.store_insights_data(data, optimization_tuple)

    def get_expanded_types(self):
        return MongoMediator.__instance.get_expanded_types()

    def get_types(self):
        return MongoMediator.__instance.get_types()

    def get_data_for_optimization(self, optimization_tuple: Tw.OptimizationTuple, time_interval: TimeInterval, ad_account_id):
        return MongoMediator.__instance.get_data_for_optimization(optimization_tuple, time_interval, ad_account_id)

    def get_existing_actor_ids(self):
        return MongoMediator.__instance.get_existing_actor_ids()

    def store_actors_metadata(self, actors_metadata):
        return MongoMediator.__instance.store_actors_metadata(actors_metadata)

    def get_parent_and_campaign_id(self, facebook_id):
        return MongoMediator.__instance.get_parent_and_campaign_id(facebook_id)

    def get_facebook_id(self, facebook_id):
        return MongoMediator.__instance.get_facebook_id(facebook_id)

    def store_goal_definitions(self, definitions):
        return MongoMediator.__instance.store_goal_definitions(definitions)

    def get_goal_display_names(self):
        return MongoMediator.__instance.get_goal_display_names()

    def log_recommendation(self, recommendation):
        return MongoMediator.__instance.log_recommendation(recommendation)

    def get_campaign_ids_by_ad_account_id(self, ad_account_id):
        return MongoMediator.__instance.get_campaign_ids_by_ad_account_id(ad_account_id)

    def get_data_for_prophet(self, optimization_tuple: Tw.OptimizationTuple, time_interval: TimeInterval):
        return MongoMediator.__instance.get_data_for_prophet(optimization_tuple, time_interval)

    def update_actor_states(self, actor_states):
        return MongoMediator.__instance.update_actor_states(actor_states)

    def get_one_campaign_data(self, campaign_id):
        return MongoMediator.__instance.get_one_campaign_data(campaign_id)

    def get_recommendations(self, number):
        return MongoMediator.__instance.get_recommendations(number)

    def get_collections(self, db_name):
        return MongoMediator.__instance.__dbClient[db_name].collection_names()



class MongoInstance(object):
    """Used to centralize fetching the required objects to interact with mongo. Creating more than one instance of this class is prohibited and will raise an exception."""
    # NOTE Newly created public methods must also be added to the above lying singelton wrapper
    __has_instance = False

    @staticmethod
    def has_instance():
        return MongoInstance.__has_instance

    def __init__(self):
        if MongoInstance.has_instance():
            raise Exception("An instance already exists!")

        connection_string = TableData.CONNECTION_STRING.value
        self.__db_client = pymongo.MongoClient(connection_string)

        optimizations_data = TableData.Optimizations.value
        db_name = optimizations_data.DB_NAME.value
        self.__db_instance = self.__db_client[db_name]

        types_coll_name = optimizations_data.OPTIMIZATION_TYPES.value
        self.__types_collection = self.__db_instance[types_coll_name]

        expanded_name = types_coll_name + optimizations_data.EXPANDED_SUFFIX.value
        self.__expanded_collection = self.__db_instance[expanded_name]

        insights_data = TableData.InsightsData.value
        store_db_name = insights_data.DB_NAME.value
        self.__store_db_instance = self.__db_client[store_db_name]

        actors_data = TableData.ActorsData.value
        actors_db_name = actors_data.DB_NAME.value
        self.__actors_db_instance = self.__db_client[actors_db_name]
        actors_collection_name = actors_data.COLLECTION_NAME.value
        self.__actors_collection = self.__actors_db_instance[actors_collection_name]

        goals_data = TableData.GoalsData.value
        goals_db_name = goals_data.DB_NAME.value
        self.__goals_db_instance = self.__db_client[goals_db_name]
        goals_collection_name = goals_data.COLLECTION_NAME.value
        self.__goals_collection = self.__goals_db_instance[goals_collection_name]

        logs_data = TableData.LogsData.value
        logs_db_name = logs_data.DB_NAME.value
        self.__logs_db_instance = self.__db_client[logs_db_name]
        recommendations_collection_name = logs_data.RECOMMENDATIONS_COLLECTION_NAME.value
        self.__recommendations_collection = self.__logs_db_instance[recommendations_collection_name]
        errors_collection_name = logs_data.ERRORS_COLLECTION_NAME.value  # This should potentially be removed. A remote logging solution should be implemented
        self.__errors_collection = self.__logs_db_instance[errors_collection_name]

        MongoInstance.__has_instance = True

    def store_optimization_types(self, types):
        self.__types_collection.drop()
        self.__types_collection.insert_many(types)

    def store_expanded_types(self, expanded_types):
        self.__expanded_collection.drop()
        self.__expanded_collection.insert_many(expanded_types)

    def store_insights_data(self, data, optimization_tuple: Tw.OptimizationTuple):
        collection_name = self.__get_optimization_colection_name(optimization_tuple)
        insights_collection = self.__store_db_instance[collection_name]
        # dropStatementHere
        # insightsCollection.drop()
        if len(data) > 0:
            insights_collection.insert_many(data)
        else:
            logging.warning(f"No data for optimization {optimization_tuple}")

    def update_actor_states(self, actor_states):
        # TODO: Remove Magic Strings
        cursor = self.__actors_collection.find()
        actors = list(cursor)
        for actor_state in actor_states:
            # update States in the ActorsInfo Collection
            state_id = str(actor_state["id"])
            state_level = actor_state["Level"]
            filtered_actors = [actor for actor in actors if actor['FiledId'] == f"{state_level}_{state_id}"]
            if len(filtered_actors) > 0:
                actor = filtered_actors[0]
                new_state_id = actor_state["StateId"]
                new_state = Tw.state_id_to_state_mapping.get(new_state_id).value
                self.__actors_collection.update_one({"FiledId": actor["FiledId"]}, {"$set": {"State": new_state}})

    def get_expanded_types(self):
        cursor = self.__expanded_collection.find({}, {"_id": 0})
        optimization_tuples = []

        for db_entry in list(cursor):
            opt_tuple = Tw.OptimizationTuple(db_entry['name'], db_entry['Level'], db_entry['Breakdown'])
            optimization_tuples.append(opt_tuple)

        return optimization_tuples

    def get_types(self):
        cursor = self.__types_collection.find({}, {"_id": 0})
        optimization_types = []
        for db_entry in list(cursor):
            opt_tuple = Tw.OptimizationType(db_entry['name'], db_entry['level'], db_entry['target'], db_entry['breakdown'])
            optimization_types.append(opt_tuple)

        return optimization_types

    def get_data_for_prophet(self, optimization_tuple: Tw.OptimizationTuple, time_interval: TimeInterval):
        collection_name = self.__get_optimization_colection_name(optimization_tuple)
        collection_instance = self.__store_db_instance[collection_name]
        time_column_name = ColumnsEnum.Where.DATE.value

        filter_query = dict()
        filter_query[time_column_name] = {}
        filter_query[time_column_name]["$gt"] = time_interval.start_date
        filter_query[time_column_name]["$lt"] = time_interval.end_date
        cursor = collection_instance.find(filter_query, {"_id": 0})
        insights_data = []

        for db_entry in list(cursor):
            insights_data.append(deepcopy(db_entry))  # This is probably redundant

        return insights_data

    def get_data_for_optimization(self, optimization_tuple: Tw.OptimizationTuple, time_interval: TimeInterval, ad_account_id):
        collection_name = self.__get_optimization_colection_name(optimization_tuple)
        collection_instance = self.__store_db_instance[collection_name]
        date_start = ColumnsEnum.Where.DATE_START.value
        date_stop = ColumnsEnum.Where.DATE_STOP.value

        filter_query = dict()
        filter_query[date_start] = {}
        # TODO: remove mizeria asta de hack cu timedate in modu' string
        filter_query[date_start]["$gt"] = '1990-01-01'
        filter_query[date_stop] = {}
        filter_query[date_stop]["$lt"] = '2150-01-01'
        filter_query[ColumnsEnum.GroupBy.AD_ACCOUNT_ID.value] = ad_account_id
        cursor = collection_instance.find(filter_query, {"_id": 0})
        insights_data = []

        for db_entry in list(cursor):
            insights_data.append(deepcopy(db_entry))  # This is probably redundant

        # insightsData = self.__get_insights_json_with_iso_date(insightsData) # Data is now properly formatted / to be deleted
        return insights_data

    def get_one_campaign_data(self, campaign_id):
        collection_name = "Budget_Campaign_None"
        collection_instance = self.__store_db_instance[collection_name]
        filter_query = {'FiledId': campaign_id}
        cursor = collection_instance.find(filter_query)
        insights_data = []
        for insight in list(cursor):
            insights_data.append(insight)
        return insights_data

    # TODO: this needs to be changed to get the new collections
    def __get_optimization_colection_name(self, optimization_tuple: Tw.OptimizationTuple):

        # TODO: check if this is okay
        result = optimization_tuple.level + '-' + optimization_tuple.breakdown + '-' + optimization_tuple.action_breakdown
        return result

    def get_existing_actor_ids(self):
        cursor = self.__actors_collection.find()  # TODO add in clause. Only get actors whose id is matching one of the newly fetched actors
        existing_actors_ids = set()
        for actor in list(cursor):
            existing_actors_ids.add(actor[Columns.INSIGHT_ACTOR_COLUMN])
        return existing_actors_ids

    def store_actors_metadata(self, actors_metadata):
        self.__actors_collection.insert_many(actors_metadata)

    def get_recommendations(self, number_of_results: int):
        return self.__recommendations_collection.find({}, {'_id': False}).limit(number_of_results)

    def log_recommendation(self, recommendation):
        self.__recommendations_collection.insert_one(recommendation)

    def get_parent_and_campaign_id(self, filed_id):
        filed_id = filed_id.split("_")[1]
        query = {"campaign_id": filed_id}
        projection = {"_id": 0}
        return self.__actors_collection.find_one(query, projection)

    def get_facebook_id(self, filed_id):
        query = {"FiledId": filed_id}
        projection = {"_id": 0, "ParentId": 0, "CampaignId": 0}
        return self.__actors_collection.find_one(query, projection)

    def __get_insights_json_with_iso_date(self, response_insights):
        response_insights = response_insights
        for insight in response_insights:
            insight_time = insight[ColumnsEnum.Where.DATE.value]
            insight[ColumnsEnum.Where.DATE.value] = TimeInterval.get_date_time_object(insight_time)
        return response_insights

    def store_goal_definitions(self, definitions):
        self.__goals_collection.drop()
        self.__goals_collection.insert_many(definitions)

        # TODO get rid of magic strings in keys for the following two methods

    def get_goal_display_names(self):
        cursor = self.__goals_collection.find()
        goal_definitions = []
        for item in list(cursor):
            goal = dict()
            goal["name"] = item["goalInternalName"]
            goal["DisplayName"] = item["goalDisplayName"]
            goal_definitions.append(goal)
        return goal_definitions

    def get_campaign_ids_by_ad_account_id(self, ad_account_id):
        query = {"ParentId": "AdAccount_" + ad_account_id}
        cursor = self.__actors_collection.find(query)
        campaign_ids = []
        for campaign_info in list(cursor):
            campaign_ids.append(campaign_info.get('FiledId'))
        return campaign_ids
