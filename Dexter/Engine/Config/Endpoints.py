_base_endpoint = 'https://dev2.filed.com'
_campaign_insights = ':42210/api/v1/'
_optimize = ':42010/api/v1/'


def get_campaing_insights_endpoint():
    return _base_endpoint + _campaign_insights


def get_optimization_endpoint():
    return _base_endpoint + _optimize
