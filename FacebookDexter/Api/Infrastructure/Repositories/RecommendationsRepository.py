from Settings.MongoConfig import MongoConfig
import pymongo
from Models.Recommendation import Recommendation
from Models.RecommendationType import RecommendationType
from Models.RecommendationStatus import RecommendationStatus
from Models.RecommendationCategory import RecommendationCategory
from datetime import datetime
from bson import ObjectId
from sshtunnel import SSHTunnelForwarder
import copy

class RecommendationsRepository(object):
    
    database_name = None
    collection_name = None
    ssh = None
    def __init__ (self, config: MongoConfig):
        self.ssh = config.sshTunnel
        mongoHost = config.mongoHost
        mongoSSHUser = config.mongoSSHUser
        mongoSSHPass = config.mongoSSHPass
        remote_bind = (config.remoteIP, config.remotePort)
        server = SSHTunnelForwarder(
            (mongoHost, 22),
            ssh_username = mongoSSHUser,
            ssh_password = mongoSSHPass,
            remote_bind_address = remote_bind
            )
        server.start()
        self.client = pymongo.MongoClient(host='127.0.0.1', port=server.local_bind_port, username=config.mongoUser, password=config.mongoPass)

        self.database_name = config.recommendationDatabaseName
        self.collection_name = config.recommendationCollectionName
        self.database = self.client[self.database_name]
        self.collection = self.database[self.collection_name]

    def get_campaigns(self, adAccountId, channel):        
        aggreagation = [
          { '$match' : {
                'ad_account_id': adAccountId,
                'channel': channel 
                }
          },
          { '$group': {
                '_id': {
                    'campaign_id': "$campaign_id",
                    'campaign_name': "$campaign_name",
                    'channel' : '$channel',
                    'ad_account_id': '$ad_account_id'
                    }
                }
          }
        ]
        cursor = self.collection.aggregate(aggreagation)
        campaigns = list(cursor)        
        distinct_campaigns = [ {'Id' : campaign['_id']['campaign_id'] , 'name' : campaign['_id']['campaign_name']} for campaign in campaigns ]
        return distinct_campaigns

    def get_recommendation_by_id(self, id: str):
        recommendation = self.collection.find_one({'_id': ObjectId(id)})
        recommendation_dict = Recommendation(recommendation).__dict__
        return recommendation_dict    

    def get_recommendations_page(self, page_number, page_size, channel, filter=None, sort=None, excluded_ids=None):
        skipped = (page_number - 1) * page_size
        query_sort = [("created_at", pymongo.DESCENDING)]
        if (sort is not None):
            query_sort = sort        
        if (excluded_ids is None):
            excluded_ids = []

        cursor, count = self.get_recommendations_by_campaign_ids(filter, excluded_ids)        
        recommendations = list(cursor.sort(query_sort).skip(skipped).limit(page_size))
        recommendations_as_dict_list = [Recommendation(retrievedRecommendation).__dict__ for retrievedRecommendation in recommendations]
        response_dict = {}
        response_dict['count'] = count
        response_dict['recommendations'] = recommendations_as_dict_list
        counts_filter = {}
        if (filter is not None):
            if ('campaign_id' in filter):
                counts_filter['campaign_id'] = {'$in': filter['campaign_id']}
        counts_by_type = self.get_counts_by_type(counts_filter);
        response_dict['countsByType'] = counts_by_type
        return response_dict

    #def get_recommendations_by_ad_account_and_level(self, adAccountId, level, channel):
    #    mongo_filter = { }
    #    mongo_filter['adAccountId'] = adAccountId
    #    mongo_filter['level'] = level
    #    mongo_filter['channel'] = channel
    #    mongo_filter['status'] = { '$nin' : [ RecommendationStatus.DISMISSED.value, RecommendationStatus.APPLIED.value ] }
    #    cursor = self.collection.find(mongo_filter)
    #    recommendationsAsDictList = [Recommendation(retrievedRecommendation).__dict__ for retrievedRecommendation in list(cursor)]
    #    return recommendationsAsDictList

    def set_recommendation_status(self, id:str, status:str):
        recommendation_objectId = ObjectId(id)
        now = datetime.now()

        self.collection.update_one({"_id" :recommendation_objectId},{'$set' : {"status": status, "application_date": now, 'applied_by': 'Dexter' }})
        return Recommendation(self.collection.find_one({"_id" : recommendation_objectId})).__dict__

    def get_action_history(self, structureId: str):
        cursor = self.collection.find({"structure_id": structureId, "status" :{ "$in" : [RecommendationStatus.APPLIED.value, RecommendationStatus.DISMISSED.value]}},
                                      {'application_details': False}).sort("application_date", pymongo.DESCENDING)
        actionHistorysAsDictList = [Recommendation(retrievedRecommendation).__dict__ for retrievedRecommendation in list(cursor)]
        return actionHistorysAsDictList

    def get_recommendations_by_campaign_ids(self, filter=None, excludedIds= None):
        query_filter = {}
        if (filter is not None):
            for key in filter:
                if (key == 'searchTerm'):
                    search_filter = {}
                    search_filter['$regex'] = filter[key]
                    search_filter['$options'] = 'i' #ignore case
                    query_filter['structure_name'] = search_filter
                    continue
                if (isinstance(filter[key], list)):
                    query_filter[key] = {"$in": filter[key]}
                else:
                    query_filter[key] = filter[key]

        if (excludedIds is not None):
            query_filter['_id'] = {'$nin': [ ObjectId(id) for id in excludedIds ]}            
        query_filter['status'] = { '$nin' : [ RecommendationStatus.DISMISSED.value, RecommendationStatus.APPLIED.value ] }
                    
        projection = {'applied_by': False, 'application_date': False, 'status': False}        
        count = self.get_count_by_filter(query_filter)
        response = self.collection.find(query_filter, projection)
        return response, count

    def get_counts_by_type(self, filter):
        counts_by_type = {}
        match_filter = copy.deepcopy(filter)
        match_filter['status'] = { '$nin' : [ RecommendationStatus.DISMISSED.value, RecommendationStatus.APPLIED.value ] }
        match_aggregation = { '$match' : match_filter}
        count_aggregation = { '$group' : {
            '_id' : '$recommendation_type',
            'count': { '$sum': 1 }
            }}
        
        aggregation = [match_aggregation, count_aggregation]
        cursor = self.collection.aggregate(aggregation)
        counts = list(cursor)

        for reco_type in RecommendationType:
            type_count = 0
            for count in counts:
                if (count['_id'] == reco_type.value):
                    type_count = count['count']

            counts_by_type[reco_type.value] = type_count

        return counts_by_type 

    def get_counts_by_category(self, filter):
        counts_by_category = {}        
        match_filter = copy.deepcopy(filter)
        match_filter['status'] = { '$nin' : [ RecommendationStatus.DISMISSED.value, RecommendationStatus.APPLIED.value ] }
        match_aggregation = { '$match' : match_filter}
        count_aggregation = { '$group' : {
            '_id' : '$category',
            'count': { '$sum': 1 }
            }}
        
        aggregation = [match_aggregation, count_aggregation]
        cursor = self.collection.aggregate(aggregation)
        counts = list(cursor)

        for metric in RecommendationCategory:
            metric_count = 0
            for count in counts:
                if (count['_id'] == metric.value):
                    metric_count = count['count']

            counts_by_category[metric.value] = metric_count
        return counts_by_category

    def get_counts(self, filter):
        types = self.get_counts_by_type(filter)
        metrics = self.get_counts_by_category(filter)
        types.update(metrics)
        return types

    def get_count_by_filter(self, filter = None):
        count_filter = {}
        if (filter is not None):
            count_filter = filter
        count = self.collection.count_documents(count_filter)
        return count




        