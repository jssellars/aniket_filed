from string import Template

import requests
from app_config.app_config import FACEBOOK_CONFIG
from forex_python.converter import CurrencyCodes
from tools.business_owner_facebook_token import get_user_token
from tools.facebook_worker import MarketingRecommendationsWorker

_facebookBudgetValidationUrl = Template(
    'https://graph.facebook.com/v5.0/$adAccountFacebookId?fields=currency,max_bid,min_daily_budget,minimum_budgets&access_token=$accessTokenFacebook')

_objectiveOptimizationCatalogs = {
    'min_daily_budget_imp': 'IMPRESSIONS',
    'min_daily_budget_video_views': 'VIDEO_VIEWS',
    'min_daily_budget_low_freq': 'APP_INSTALLS',
    'min_daily_budget_high_freq': ['LINK_CLICK', 'PAGE_LIKES']
}


def _MapMinimumBudgetsResponse(minimumBudgetsFacebook, currency):
    minimumBudgets = list(filter(lambda x: x if x['currency'] == currency else None, minimumBudgetsFacebook))[0]

    if not minimumBudgets:
        return

    mappendMinimumBudgets = {
        'IMPRESSIONS': round(minimumBudgets['min_daily_budget_imp'] / 100),
        'VIDEO_VIEWS': round(minimumBudgets['min_daily_budget_video_views'] / 100),
        'APP_INSTALLS': round(minimumBudgets['min_daily_budget_low_freq'] / 100),
        'LINK_CLICK': round(minimumBudgets['min_daily_budget_high_freq'] / 100),
        'PAGE_LIKES': round(minimumBudgets['min_daily_budget_high_freq'] / 100),
        'DEFAULT': round(minimumBudgets['min_daily_budget_high_freq'] / 100),
    }

    return mappendMinimumBudgets


def _MapBudgetValidationResponse(facebookResponse):
    _currencyConverter = CurrencyCodes()
    mappedBudgetValidationResponse = {
        'currency': facebookResponse['currency'],
        'currencySymbol': _currencyConverter.get_symbol(facebookResponse['currency']),
        'maximumAdAccountBid': round(facebookResponse['max_bid']['data'][0]['max_bid'] / 100),
        'minimumAdAccountDailyBudget': round(facebookResponse['min_daily_budget'] / 100),
        'minimumAdAccountBudgets': _MapMinimumBudgetsResponse(facebookResponse['minimum_budgets']['data'],
                                                              facebookResponse['currency'])
    }

    return mappedBudgetValidationResponse


def GetBudgetValidationCatalogHandler(businessOwnerFacebookId, adAccountFacebookId):
    token = get_user_token(business_owner_facebook_id=businessOwnerFacebookId)

    url = _facebookBudgetValidationUrl.substitute(adAccountFacebookId=adAccountFacebookId,
                                                  accessTokenFacebook=token)
    responseFacebook = requests.get(url)
    responseFacebook = responseFacebook.json()

    if 'error' in responseFacebook.keys():
        if 'error_user_msg' in responseFacebook['error'].keys():
            response = {
                'message': responseFacebook['error']['message'],
                'error_usr_message': responseFacebook['error']['error_user_msg'],
                'error_user_title': responseFacebook['error']['error_user_title']}
        elif 'error_user_msg' not in responseFacebook['error'].keys():
            response = {
                'message': responseFacebook['error']['message'],
                'error_usr_message': 'An unknown error has accured; %s. Please try again or contact support.' %
                                     responseFacebook['error']['message'],
                'error_user_title': 'Unknown error'}

    else:
        response = _MapBudgetValidationResponse(responseFacebook)

    return response


def GetMarketingRecommendationsHandler(businessOwnerFacebookId, adAccountFacebookId, level):
    try:
        worker = MarketingRecommendationsWorker(business_owner_facebook_id=businessOwnerFacebookId,
                                                facebook_config=FACEBOOK_CONFIG)

        results = worker.GetRecommendations(adAccountFacebookId, level)
    except Exception as e:
        raise e

    return results
