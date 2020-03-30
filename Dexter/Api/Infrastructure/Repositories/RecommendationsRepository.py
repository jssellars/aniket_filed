from Settings.MongoConfig import MongoConfig
import pymongo
from Models.Recommendation import Recommendation
from Models.RecommendationType import RecommendationType
from Models.RecommendationStatus import RecommendationStatus
from Models.RecommendationMetric import RecommendationMetric
from datetime import datetime
from bson import ObjectId
from sshtunnel import SSHTunnelForwarder

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
        campaigns = self.collection.find({'adAccountId' : adAccountId, 'channel' : channel }).distinct('campaignId')
        aggreagation = [ { '$group': {
                                    '_id': {
                                        'campaignId': "$campaignId",
                                        'campaignName': "$campaignName",
                                        'channel' : '$channel',
                                        'adAccountId': '$adAccountId'}
                                    }
                        }]
        cursor = self.collection.aggregate(aggreagation)
        campaigns = list(cursor)
        # TODO: find a way to filter in the mongo aggregation pipeline
        campaigns = [campaign for campaign in campaigns if (campaign['_id']['channel'] == channel and campaign['_id']['adAccountId'] == adAccountId)]

        distinct_campaigns = [ {'Id' : campaign['_id']['campaignId'] , 'name' : campaign['_id']['campaignName']} for campaign in campaigns ]
        return distinct_campaigns

    def get_recommendation_by_id(self, id: str):
        recommendation = self.collection.find_one({'_id': ObjectId(id)})
        recommendation_dict = Recommendation(recommendation).__dict__
        return recommendation_dict    

    def get_recommendations_page(self, campaign_ids, page_number, page_size, channel, filter=None, sort=None, excluded_ids=None):
        skipped = (page_number - 1) * page_size
        query_sort = [("createdAt", pymongo.DESCENDING)]
        if (sort is not None):
            query_sort = sort        
        if (excluded_ids is None):
            excluded_ids = []

        cursor, count = self.get_recommendations_by_campaign_ids(campaign_ids, filter, excluded_ids)        
        recommendations = list(cursor.sort(query_sort).skip(skipped).limit(page_size))
        recommendations_as_dict_list = [Recommendation(retrievedRecommendation).__dict__ for retrievedRecommendation in recommendations]
        response_dict = {}
        response_dict['count'] = count
        response_dict['recommendations'] = recommendations_as_dict_list
        counts_by_type = self.get_counts_by_type(campaign_ids, channel);
        response_dict['countsByType'] = counts_by_type
        return response_dict

    def get_recommendations_by_ad_account_and_level(self, adAccountId, level, channel):
        mongo_filter = { }
        mongo_filter['adAccountId'] = adAccountId
        mongo_filter['level'] = level
        mongo_filter['channel'] = channel
        mongo_filter['status'] = { '$nin' : [ RecommendationStatus.DISMISSED.value, RecommendationStatus.APPLIED.value ] }
        cursor = self.collection.find(mongo_filter)
        recommendationsAsDictList = [Recommendation(retrievedRecommendation).__dict__ for retrievedRecommendation in list(cursor)]
        return recommendationsAsDictList

    def set_recommendation_status(self, id:str, status:str):
        recommendation_objectId = ObjectId(id)
        now = datetime.now()
        self.collection.update_one({"_id" :recommendation_objectId},{'$set' : {"status": status, "applicationDate": now, 'appliedBy': 'Dexter' }})
        return Recommendation(self.collection.find_one({"_id" : recommendation_objectId})).__dict__

    def get_action_history(self, structureId: str):
        cursor = self.collection.find({"structureId": structureId, "status" :{ "$in" : [RecommendationStatus.APPLIED.value, RecommendationStatus.DISMISSED.value]}},
                                      {'applicationDetails': False})
        actionHistorysAsDictList = [Recommendation(retrievedRecommendation).__dict__ for retrievedRecommendation in list(cursor)]
        return actionHistorysAsDictList

    def get_recommendations_by_campaign_ids(self, campaignIds, filter=None, excludedIds= None):        
        filterValues = {'$in' : campaignIds}
        queryFilter = {'campaignId' : filterValues}
        if (filter is not None):
            for key in filter:
                if (key == 'searchTerm'):
                    searchFilter = {}
                    searchFilter['$regex'] = filter[key]
                    searchFilter['$options'] = 'i' #ignore case
                    queryFilter['structureName'] = searchFilter
                    continue
                if (isinstance(filter[key], list)):
                    queryFilter[key] = {"$in": filter[key]}
                else:
                    queryFilter[key] = filter[key]
        if (excludedIds is not None):
            queryFilter['_id'] = {'$nin': [ ObjectId(id) for id in excludedIds ]}            
        queryFilter['status'] = { '$nin' : [ RecommendationStatus.DISMISSED.value, RecommendationStatus.APPLIED.value ] }
                    
        projection = {'applicationDetails' : False, 'appliedBy': False, 'applicationDate': False, 'status': False}        
        count = self.get_count_by_filter(queryFilter)
        response = self.collection.find(queryFilter, projection)
        return response, count

    def get_counts_by_type(self, campaignIds, channel):
        filter_values = {'$in' : campaignIds}
        query_filter = {'campaignId' : filter_values}
        counts_by_type = {}
        for reco_type in RecommendationType:
            typed_filter = query_filter
            typed_filter['recommendationType'] = reco_type.value
            typed_filter['status'] = { '$nin' : [ RecommendationStatus.DISMISSED.value, RecommendationStatus.APPLIED.value ] }
            type_count = self.get_count_by_filter(typed_filter, channel)            
            counts_by_type[reco_type.value] = type_count
        return counts_by_type 

    def get_counts_by_metrics(self, campaignIds, channel):
        filter_values = { '$in' : campaignIds }
        query_filter = { 'campaignId' : filter_values}
        counts_by_metrics = {}
        # TODO: move the list of metrics to an outside resource
        for metric in RecommendationMetric:
            metric_filter = query_filter
            metric_filter['metric'] = metric.value
            metric_filter['status'] = { '$nin' : [ RecommendationStatus.DISMISSED.value, RecommendationStatus.APPLIED.value ] }
            metric_count = self.get_count_by_filter(metric_filter, channel)
            counts_by_metrics[metric.value] = metric_count
        return counts_by_metrics

    def get_counts(self, campaignsIds, channel):
        types = self.get_counts_by_type(campaignsIds, channel)
        metrics = self.get_counts_by_metrics(campaignsIds, channel)
        types.update(metrics)
        return types

    def get_count_by_filter(self, filter = None, channel = None):
        count_filter = {}
        if (filter is not None):
            count_filter = filter
        if (channel is not None):
            if (isinstance(channel, list)):
                count_filter['channel'] = {'$in': channel}
            else:
                count_filter['channel'] = channel

        count = self.collection.count_documents(count_filter)
        return count




        