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
from Tools.ImportanceMapper import ImportanceMapper
import requests

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

    permittedFilters = ['campaign_id', 'channel', 'category', 'optimization_type', 'level', 'importance', 'confidence',
                       'recommendation_type', 'source', 'structure_id', 'ad_account_id', 'search_term', 'parent_id']

    permitted_sort_criteria = ['recommendation_type', 'optimization_type', 'created_at', 'importance', 'confidence']
    data = request.get_json()        

    pageNumber = data['PageNumber'] if 'PageNumber' in data else 1
    if (pageNumber is None):
        pageNumber = 1

    pageSize = data['PageSize'] if 'PageSize' in data else 10
    if (pageSize is None):
        pageSize = 10   


    filter = data['Filter'] if 'Filter' in data else None

    if filter is not None:
        channel = data['Filter']['channel'] if 'channel' in data['Filter'] else 'facebook'
    else:
        channel='facebook'

    bad_filters = []
    if (filter is not None):
        if (isinstance(filter, dict) == False):
             return 'invalid filter', 400
        for key in filter:
            if key not in permittedFilters:
                return f"invalid filter criterion {key}", 400            
            if filter[key] == []:
                bad_filters.append(key)
            if key in ['importance']:
                mappedValues = []
                for value in filter[key]:
                    mappedValues.append(ImportanceMapper.get_importance_value(value))
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
            if key not in permitted_sort_criteria:
                return f'invalid sort criterion {key}', 400
            if sort[key] not in ['Ascending', 'Descending']:
                return f'invalid sort order, {sort[key]}', 400
            if sort[key] == 'Ascending':
                mongoSort.append((key, 1))
            else:
                mongoSort.append((key, -1))
    filter['confidence'] = {'$gte' : 0.5 }

    try :
        recommendationsList = recommendation_repository.get_recommendations_page(pageNumber, pageSize, channel, filter, mongoSort, excludedIds)
        response = make_response((json.dumps(recommendationsList)))
        response.headers['Content-Type'] = "application/json"
        return response
    except Exception as e:
        print (e)
        return 500, 'An error occcured'

@app.route('/ApplyRecommendation', methods=['PATCH'])
def applyRecommendation():
    id = request.args.get('id')
    headers = request.headers
    
    bearer = headers.get('HTTP_AUTHORIZATION')
    print(bearer)
    try:
        recommendation = recommendation_repository.get_recommendation_by_id(id)
    except Exception as e:
        print (e)
        return 500, 'An error occcured'

    details = recommendation.get('applicationDetails', None)
    if (details is None):
        return 400, 'Unable to apply recommendation'
    
    request_payload = details
    request_header = { 'HTTP_AUTHORIZATION' : bearer }
    url = "https://dev.filed.com:42220/api/v1/"
    url += recommendation['level'] + '/'
    url += recommendation['structureId']    
    try:
        apply_request = requests.put(url, request_payload, headers=request_header);
        if (apply_request.status_code == 200):
            applieddRecommendation = recommendation_repository.set_recommendation_status(id, RecommendationStatus.APPLIED.value)
            if (applieddRecommendation['status'] == RecommendationStatus.APPLIED.value):
                response = make_response({})
                response.headers['Content-Type'] = "application/json"
                return response
        else:
            return 'unable to apply recommendation', 500            

    except Exception as e:
        print (e)
        return 500, 'An error occcured'

@app.route('/DismissRecommendation', methods=['PATCH'])
def dismissRecommendation():
    try:
        id = request.args.get('id')
        dismmissedRecommendation = recommendation_repository.set_recommendation_status(id, RecommendationStatus.DISMISSED.value)
        if (dismmissedRecommendation['status'] == RecommendationStatus.DISMISSED.value):
            response = make_response({})
            response.headers['Content-Type'] = "application/json"
            return response
        else:
            return 'unable to reject recommendation', 500
    except Exception as e:
        print (e)
        return 500, 'An error occcured'

@app.route('/GetRecommendation')
def GetRecommendationById():
    try:
        id = request.args.get('id')
        recommendation = recommendation_repository.get_recommendation_by_id(id)
        response = make_response((json.dumps(recommendation)))
        response.headers['Content-Type'] = "application/json"
        return response
    except Exception as e:
        print (e)
        return 500, 'An error occcured'

@app.route('/GetCampaigns')
def GetCampaings():   
    try:
        adAcccountId = request.args.get('adAccountId')
        channel = request.args.get('channel')
        campaigns = recommendation_repository.get_campaigns(adAcccountId, channel)
        response = make_response((json.dumps(campaigns)))
        response.headers['Content-Type'] = "application/json"
        return response
    except Exception as e:
        print (e)
        return 500, 'An error occcured'

@app.route('/GetRecommendations')
def GetRecommendations():
    try:
        adAcccountId = request.args.get('adAccountId')
        channel = request.args.get('channel')
        level = request.args.get('level')
        recommendations = recommendation_repository.get_recommendations_by_ad_account_and_level(adAcccountId, level, channel)
        response = make_response(json.dumps(recommendations))
        response.headers['Content-Type'] = "application/json"
        return response
    except Exception as e:
        print (e)
        return 500, 'An error occcured'


@app.route('/GetActionHistory')
def GetActionHistory():
    try:
        structureId = request.args.get('structureId')
        history = recommendation_repository.get_action_history(structureId)
        response = make_response(json.dumps(history))
        return response
    except Exception as e:
        print (e)
        return 500, 'An error occcured'

@app.route('/GetCountByCategory', methods=['POST'])
def getCountsByCategory():
    try:        
        data = request.get_json()
        campaign_ids = data['campaignIds']
        channel = data['channel']
        count_filter = {}

        if (isinstance(campaign_ids, list)):
            count_filter['campaign_id'] = {'$in': campaign_ids}
        else:
            count_filter['campaign_id'] = campaign_ids

        if (isinstance(channel, list)):
            count_filter['channel'] = {'$in': channel}
        else:
            count_filter['channel'] = channel        

        counts = recommendation_repository.get_counts(count_filter)
        response = make_response(json.dumps(counts))
        return response
    except Exception as e:
        print (e)
        return 500, 'An error occcured'

if __name__ == '__main__':        

    with open(path.abspath('Settings/JSON/app.settings.dev.json')) as appsettings:
        configDict = json.load(appsettings)
        mongoConfig = MongoConfig(configDict['mongoDatabase'])
        recommendation_repository = RecommendationsRepository(mongoConfig)
        app_config = configDict['flaskApp']
        flask_host = app_config['flask_host']
        PORT = app_config['flask_port']        
    
    app.run(flask_host, PORT)
    