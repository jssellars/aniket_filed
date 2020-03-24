from Settings.MongoConfig import MongoConfig
import pymongo
from Models.Recommendation import Recommendation
from Models.RecommendationType import RecommendationType
from Models.RecommendationStatus import RecommendationStatus
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

    def getCampaigns(self, adAccountId, channel):
        campaigns = self.collection.find({'adAccountId' : adAccountId, 'channel' : channel }).distinct('campaignId')
        aggreagation = [ { '$group': {
                                    '_id': {
                                        'campaignId': "$campaignId",
                                        'campaignName': "$campaignName",
                                        'channel' : '$channel'}
                                    }
                        }]
        cursor = self.collection.aggregate(aggreagation)
        campaigns = list(cursor)
        # TODO: remove this hack, here we check so the channel is the one we want
        campaigns = [campaign for campaign in campaigns if campaign['_id']['channel'] == channel]

        distinct_campaigns = [ {'Id' : campaign['_id']['campaignId'] , 'name' : campaign['_id']['campaignName']} for campaign in campaigns ]
        return distinct_campaigns

    def getRecommendationById(self, id: str):
        recommendation = self.collection.find_one({'_id': ObjectId(id)})
        recommendationDict = Recommendation(recommendation).__dict__
        return recommendationDict    

    def getRecommendationsPage(self, campaignIds, pagenumber, pagesize, channel, filter=None, sort=None, excludedIds=None):
        skipped = (pagenumber - 1) * pagesize
        querySort = [("createdAt", pymongo.DESCENDING)]
        if (sort is not None):
            querySort = sort        
        if (excludedIds is None):
            excludedIds = []

        cursor, count = self.getRecommendationsByCampaignIds(campaignIds, filter, excludedIds)        
        recommendations = list(cursor.sort(querySort).skip(skipped).limit(pagesize))
        recommendationsAsDictList = [Recommendation(retrievedRecommendation).__dict__ for retrievedRecommendation in recommendations]
        responseDict = {}
        responseDict['count'] = count
        responseDict['recommendations'] = recommendationsAsDictList
        countsByType = self.getCountsByType(campaignIds, channel);
        responseDict['countsByType'] = countsByType
        return responseDict

    def getRecommendationsByAdAccountAndLevel(self, adAccountId, level, channel):
        mongoFilter = { }
        mongoFilter['adAccountId'] = adAccountId
        mongoFilter['level'] = level
        mongoFilter['channel'] = channel
        mongoFilter['status'] = { '$nin' : [ RecommendationStatus.Dismissed.value, RecommendationStatus.Applied.value ] }
        cursor = self.collection.find(mongoFilter)
        recommendationsAsDictList = [Recommendation(retrievedRecommendation).__dict__ for retrievedRecommendation in list(cursor)]
        return recommendationsAsDictList

    def setRecommendationStatus(self, id:str, status:str):
        recommendationObjectId = ObjectId(id)
        now = datetime.now()
        self.collection.update_one({"_id" :recommendationObjectId},{'$set' : {"status": status, "applicationDate": now, 'appliedBy': 'Dexter' }})
        return Recommendation(self.collection.find_one({"_id" : recommendationObjectId})).__dict__

    def getActionHistory(self, structureId: str):
        cursor = self.collection.find({"structureId": structureId, "status" :{ "$in" : [RecommendationStatus.Applied.value, RecommendationStatus.Dismissed.value]}},
                                      {'applicationDetails': False})
        actionHistorysAsDictList = [Recommendation(retrievedRecommendation).__dict__ for retrievedRecommendation in list(cursor)]
        return actionHistorysAsDictList

    def getRecommendationsByCampaignIds(self, campaignIds, filter=None, excludedIds= None):        
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
        queryFilter['status'] = { '$nin' : [ RecommendationStatus.Dismissed.value, RecommendationStatus.Applied.value ] }
                    
        projection = {'applicationDetails' : False, 'appliedBy': False, 'applicationDate': False, 'status': False}        
        count = self.getCountByFilter(queryFilter)
        response = self.collection.find(queryFilter, projection)
        return response, count

    def getCountsByType(self, campaignIds, channel):
        filterValues = {'$in' : campaignIds}
        queryFilter = {'campaignId' : filterValues}
        countsByType = {}
        for recoType in RecommendationType:
            typedFilter = queryFilter
            typedFilter['recommendationType'] = recoType.value
            typedFilter['status'] = { '$nin' : [ RecommendationStatus.Dismissed.value, RecommendationStatus.Applied.value ] }
            typeCount = self.getCountByFilter(typedFilter, channel)
            countsByType[recoType.value] = typeCount
        return countsByType

    def getCountByFilter(self, filter = None, channel = None):
        if channel:
            if not isinstance(channel, list):
                channel = [channel]
            filterByChannel = {'channel' : {'$in': channel}}

            docs = self.collection.count_documents(filterByChannel)
            if docs == 0:
                return 0

        if (filter is not None):
            return self.collection.count_documents(filter)
            
        return self.collection.count_documents()




        