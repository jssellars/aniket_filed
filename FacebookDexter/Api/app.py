import json
import os
from os import path

import requests
from Infrastructure.Repositories.RecommendationsRepository import RecommendationsRepository
from Models.RecommendationStatus import RecommendationStatus
from Models.RuleRedirect import RuleRedirectEnum
from Models.TuringEndpointEnum import TuringEndpointEnum
from Settings.MongoConfig import MongoConfig
from Tools.ImportanceMapper import ImportanceMapper
from flask import Flask, make_response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

env = os.environ.get("PYTHON_ENV")
if not env:
    env = "dev"


@app.route('/')
def hello():
    return "Hello World!!!"


@app.route('/GetRecommendationsPage', methods=['POST'])
def get_recommendations_page():
    permitted_filters = ['campaign_id', 'channel', 'category', 'optimization_type', 'level', 'importance', 'confidence',
                         'recommendation_type', 'source', 'structure_id', 'ad_account_id', 'search_term', 'parent_id']

    permitted_sort_criteria = ['recommendation_type', 'optimization_type', 'created_at', 'importance', 'confidence']
    data = request.get_json()

    page_number = data['PageNumber'] if 'PageNumber' in data else 1
    if page_number is None:
        page_number = 1

    page_size = data['PageSize'] if 'PageSize' in data else 10
    if page_size is None:
        page_size = 10

    _filter = data['Filter'] if 'Filter' in data else {}

    if _filter:
        channel = data['Filter']['channel'] if 'channel' in data['Filter'] else 'facebook'
    else:
        channel = 'facebook'

    bad_filters = []
    if _filter:
        if not isinstance(_filter, dict):
            return 'invalid filter', 400
        for key in _filter:
            if key not in permitted_filters:
                return f"invalid filter criterion {key}", 400
            if not _filter[key]:
                bad_filters.append(key)
            if key in ['importance']:
                mapped_values = []
                for value in _filter[key]:
                    mapped_values.append(ImportanceMapper.get_importance_value(value))
                _filter[key] = mapped_values

        for key in bad_filters:
            del _filter[key]

    excluded_ids = data['ExcludedIds'] if 'ExcludedIds' in data else None

    sort = []
    if 'Sort' in data:
        sort = data['Sort']

    mongo_sort = None
    if sort:
        mongo_sort = []
        if not isinstance(sort, dict):
            return 'invalid sort', 400
        for key in sort:
            if key not in permitted_sort_criteria:
                return f'invalid sort criterion {key}', 400
            if sort[key] not in ['Ascending', 'Descending']:
                return f'invalid sort order, {sort[key]}', 400
            if sort[key] == 'Ascending':
                mongo_sort.append((key, 1))
            else:
                mongo_sort.append((key, -1))
    _filter['confidence'] = {'$gte': 0.5}

    try:
        recommendations_list = recommendation_repository.get_recommendations_page(page_number, page_size, channel, _filter, mongo_sort, excluded_ids)
        response = make_response((json.dumps(recommendations_list)))
        response.headers['Content-Type'] = "application/json"
        return response
    except Exception as e:
        print(e)
        return 500, 'An error occcured'


@app.route('/ApplyRecommendation', methods=['PATCH'])
def apply_recommendation():
    recommendation_id = request.args.get('id')
    headers = request.headers

    bearer = headers.get('HTTP_AUTHORIZATION')
    try:
        recommendation = recommendation_repository.get_recommendation_by_id(recommendation_id)
    except Exception as e:
        print(e)
        return 500, 'An error occcured'

    details = recommendation.get('applicationDetails', None)
    if details is None:
        return 400, 'Unable to apply recommendation'

    request_payload = details
    request_header = {'HTTP_AUTHORIZATION': bearer}

    url = TuringEndpointEnum(env.upper()).value
    url += recommendation['level'] + '/'
    structure_id = recommendation['structureId']
    url += structure_id

    try:
        if recommendation['redirect_for_edit'] == RuleRedirectEnum.DUPLICATE.value:
            url += '/duplicate'
            apply_request = requests.post(url, request_payload, headers=request_header)
        else:
            apply_request = requests.put(url, request_payload, headers=request_header)
        if apply_request.status_code == 200:
            recommendation_repository.set_recommendation_statuses_by_structure_id(structure_id, RecommendationStatus.DISMISSED.value)
            applied_recommendation = recommendation_repository.set_recommendation_status(recommendation_id, RecommendationStatus.APPLIED.value)
            if applied_recommendation['status'] == RecommendationStatus.APPLIED.value:
                response = make_response({})
                response.headers['Content-Type'] = "application/json"
                return response
        else:
            return 'unable to apply recommendation', 500

    except Exception as e:
        print(e)
        return 500, 'An error occcured'


@app.route('/DismissRecommendation', methods=['PATCH'])
def dismiss_recommendation():
    try:
        recommendation_id = request.args.get('id')
        dismissed_recommendation = recommendation_repository.set_recommendation_status(recommendation_id, RecommendationStatus.DISMISSED.value)
        if dismissed_recommendation['status'] == RecommendationStatus.DISMISSED.value:
            response = make_response({})
            response.headers['Content-Type'] = "application/json"
            return response
        else:
            return 'unable to reject recommendation', 500
    except Exception as e:
        print(e)
        return 500, 'An error occcured'


@app.route('/GetRecommendation')
def get_recommendation_by_id():
    try:
        recommendation_id = request.args.get('id')
        recommendation = recommendation_repository.get_recommendation_by_id(recommendation_id)
        response = make_response((json.dumps(recommendation)))
        response.headers['Content-Type'] = "application/json"
        return response
    except Exception as e:
        print(e)
        return 500, 'An error occcured'


@app.route('/GetCampaigns')
def get_campaings():
    try:
        ad_account_id = request.args.get('adAccountId')
        channel = request.args.get('channel')
        campaigns = recommendation_repository.get_campaigns(ad_account_id, channel)
        response = make_response((json.dumps(campaigns)))
        response.headers['Content-Type'] = "application/json"
        return response
    except Exception as e:
        print(e)
        return 500, 'An error occcured'


@app.route('/GetActionHistory')
def get_action_history():
    try:
        structure_id = request.args.get('structureId')
        history = recommendation_repository.get_action_history(structure_id)
        response = make_response(json.dumps(history))
        return response
    except Exception as e:
        print(e)
        return 500, 'An error occcured'


@app.route('/GetCountByCategory', methods=['POST'])
def get_counts_by_category():
    try:
        data = request.get_json()
        campaign_ids = data['campaignIds']
        channel = data['channel']
        count_filter = {}

        if isinstance(campaign_ids, list):
            count_filter['campaign_id'] = {'$in': campaign_ids}
        else:
            count_filter['campaign_id'] = campaign_ids

        if isinstance(channel, list):
            count_filter['channel'] = {'$in': channel}
        else:
            count_filter['channel'] = channel

        counts = recommendation_repository.get_counts(count_filter)
        response = make_response(json.dumps(counts))
        return response
    except Exception as e:
        print(e)
        return 500, 'An error occcured'


if __name__ == '__main__':
    with open(path.abspath(f'Settings/JSON/app.settings.{env}.json')) as app_settings:
        config_dict = json.load(app_settings)
        mongo_config = MongoConfig(config_dict.get('mongoDatabase'))
        recommendation_repository = RecommendationsRepository(mongo_config)
        app_config = config_dict['flaskApp']
        flask_host = app_config['flask_host']
        port = app_config['flask_port']
        debug = app_config['debug']

    app.run(debug=debug, host=flask_host, port=port)
