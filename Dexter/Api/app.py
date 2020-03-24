from flask import Flask, make_response, request
from flask_restful import Resource, Api
from os import path
import sys
import json
from Settings.MongoConfig import MongoConfig
import os
from Models.Recommendation import Recommendation
from bson import BSON
from Infrastructure.Repositories.RecommendationsRepository import RecommendationsRepository
from flask_cors import CORS
from Models.RecommendationStatus import RecommendationStatus
from Tools.ConfidenceImportanceMapper import ConfidenceImportanceMapper

app = Flask(__name__)
CORS(app)
#api = Api(app)

mongoConfig = None
recommendationRepository = None
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def hello():   
    return "Hello World!!!"

@app.route('/GetRecommendationsPage', methods = ['POST'])
def GetRecommendationsPage():
    data = request.get_json()

    if ('CampaignIds' not in data):
        return 'please provide Campaing Ids', 400
        
    campaignIds = data['CampaignIds']
    if (campaignIds is None):
        campaignIds = []

    pageNumber = data['PageNumber'] if 'PageNumber' in data else 1
    if (pageNumber is None):
        pageNumber = 1

    pageSize = data['PageSize'] if 'PageSize' in data else 10
    if (pageSize is None):
        pageSize = 10   


    filter = data['Filter'] if 'Filter' in data else None

    if filter:
        channel = data['Filter']['channel'] if 'channel' in data['Filter'] else 'facebook'

    bad_filters = []
    if (filter is not None):
        if (isinstance(filter, dict) == False):
             return 'invalid filter', 400
        for key in filter:
            if key not in ['source', 'level', 'confidence', 'importance', 'recommendationType', 'optimizationType', 'structureId', 'metric', 'channel', 'searchTerm']:
                return f"invalid filter criterion {key}", 400            
            if filter[key] == []:
                bad_filters.append(key)
            if key in ['confidence' , 'importance']:
                mappedValues = []
                for value in filter[key]:
                    mappedValues.append(ConfidenceImportanceMapper.getConfidenceImportanceValue(value))
                filter[key] = mappedValues
                
    
        for key in bad_filters:
            del filter[key]    
    
    excludedIds = data['ExcludedIds'] if 'ExcludedIds' in data else None

    sort = None
    if ('Sort' in data):
        sort = data['Sort']

    mongoSort = None
    if (sort is not None):
        mongoSort = []
        if (isinstance(sort, dict) == False):
            return 'invalid sort', 400
        for key in sort:
            if key not in ['recommendationType', 'optimizationType', 'createdAt', 'importance', 'confidence']:
                return f'invalid sort criterion {key}', 400
            if sort[key] not in ['Ascending', 'Descending']:
                return f'invalid sort order, {sort[key]}', 400
            if sort[key] == 'Ascending':
                mongoSort.append((key, 1))
            else:
                mongoSort.append((key, -1))

    recommendationsList = recommendationRepository.getRecommendationsPage(campaignIds, pageNumber, pageSize, channel, filter, mongoSort, excludedIds)
    response = make_response((json.dumps(recommendationsList)))
    response.headers['Content-Type'] = "application/json"
    return response


@app.route('/ApplyRecommendation', methods=['PATCH'])
def applyRecommendation():
    id = request.args.get('id')
    applieddRecommendation = recommendationRepository.setRecommendationStatus(id, RecommendationStatus.Applied.value)
    if (applieddRecommendation['status'] == RecommendationStatus.Applied.value):
        response = make_response({})
        response.headers['Content-Type'] = "application/json"
        return response
    else:
        return 'unable to apply recommendation', 500

@app.route('/DismissRecommendation', methods=['PATCH'])
def dismissRecommendation():
    id = request.args.get('id')
    dismmissedRecommendation = recommendationRepository.setRecommendationStatus(id, RecommendationStatus.Dismissed.value)
    if (dismmissedRecommendation['status'] == RecommendationStatus.Dismissed.value):
        response = make_response({})
        response.headers['Content-Type'] = "application/json"
        return response
    else:
        return 'unable to reject recommendation', 500

@app.route('/GetRecommendation')
def GetRecommendationById():
    id = request.args.get('id')
    recommendation = recommendationRepository.getRecommendationById(id)
    response = make_response((json.dumps(recommendation)))
    response.headers['Content-Type'] = "application/json"
    return response    

@app.route('/GetCampaigns')
def GetCampaings():    
    adAcccountId = request.args.get('adAccountId')
    channel = request.args.get('channel')
    campaigns = recommendationRepository.getCampaigns(adAcccountId, channel)
    response = make_response((json.dumps(campaigns)))
    response.headers['Content-Type'] = "application/json"
    return response

@app.route('/GetRecommendations')
def GetRecommendations():
    adAcccountId = request.args.get('adAccountId')
    channel = request.args.get('channel')
    level = request.args.get('level')
    recommendations = recommendationRepository.getRecommendationsByAdAccountAndLevel(adAcccountId, level, channel)
    response = make_response(json.dumps(recommendations))
    response.headers['Content-Type'] = "application/json"
    return response


@app.route('/GetActionHistory')
def GetActionHistory():
    structureId = request.args.get('structureId')
    history = recommendationRepository.getActionHistory(structureId)
    response = make_response(json.dumps(history))
    return response

if __name__ == '__main__':    
    flask_host = os.environ.get('SERVER_HOST', 'localhost')

    with open(path.abspath('Settings/JSON/app.settings.dev.json')) as appsettings:
        configDict = json.load(appsettings)
        mongoConfig = MongoConfig(configDict['mongoDatabase'])
        recommendationRepository = RecommendationsRepository(mongoConfig)
        
    PORT = 42010
    app.run(flask_host, PORT)
    