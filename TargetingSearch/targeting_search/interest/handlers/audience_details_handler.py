import requests
import scipy.interpolate
from app_config.app_config import AUDIENCE_DETAILS_URL
from app_config.app_config import FACEBOOK_CONFIG
from numpy import ceil


def _EstimateDeliveryResults(dailyOutcomesCurve, estimatedDailyAudienceSize, estimatedMonthlyAudienceSize, budget):
    # Map FB response
    spend = [dailyOutcome['spend'] / 100 for dailyOutcome in dailyOutcomesCurve]
    minimumEstimatedReachBySpend = [dailyOutcome['reach_lower_bound'] for dailyOutcome in dailyOutcomesCurve]
    maximumEstimatedReachBySpend = [dailyOutcome['reach_upper_bound'] for dailyOutcome in dailyOutcomesCurve]
    minimumEstimatedActionsBySpend = [dailyOutcome['actions_lower_bound'] for dailyOutcome in dailyOutcomesCurve]
    maximumEstimatedActionsBySpend = [dailyOutcome['actions_upper_bound'] for dailyOutcome in dailyOutcomesCurve]

    # Interpolate FB response
    minimumEstimatedReachBySpend1DInterpl = scipy.interpolate.interp1d(spend, minimumEstimatedReachBySpend)
    maximumEstimatedReachBySpend1DInterpl = scipy.interpolate.interp1d(spend, maximumEstimatedReachBySpend)

    minimumEstimatedActionsBySpend1DInterpl = scipy.interpolate.interp1d(spend, minimumEstimatedActionsBySpend)
    maximumEstimatedActionsBySpend1DInterpl = scipy.interpolate.interp1d(spend, maximumEstimatedActionsBySpend)

    estimatedResults = {
        'estimatedMonthlyAudienceSize': estimatedMonthlyAudienceSize,
        'estimatedDailyAudienceSize': estimatedDailyAudienceSize,
        'minimumEstimatedReach': int(ceil(minimumEstimatedReachBySpend1DInterpl(budget))),
        'maximumEstimatedReach': int(ceil(maximumEstimatedReachBySpend1DInterpl(budget))),
        'minimumEstimatedActions': int(ceil(minimumEstimatedActionsBySpend1DInterpl(budget))),
        'maximumEstimatedActions': int(ceil(maximumEstimatedActionsBySpend1DInterpl(budget)))
    }

    return estimatedResults


def EstimateAudienceSize(request=None):
    # try:
    #     token = get_user_token(request['business_owner_facebook_id'])
    # except KeyError:
    #     token = FACEBOOK_CONFIG['permanent_token']
    token = 'EAABsbCS1iHgBAM4zTDFECOIkR8UPJ7diIwjsFaYWpXZCfhEX56eHSQXZB0XlZB6ZAuPZCUAFL6zf5UwuSz0sUWOvIrmyQI5V1JQJZBkv3QVa8l7kGJHpEL3vVZBS9PFnZC7gDA7hiNSo2lZB2AiZCTxCM8Pxi7UaZB0N16wzWvfZCXFoGUyZCJNeZBPkW4B5XIyZCePQNEZD'  # FACEBOOK_CONFIG['permanent_token']
    url = AUDIENCE_DETAILS_URL.substitute(apiVersion=FACEBOOK_CONFIG["api_version"],
                                          adAccountFacebookId=request["ad_account_id"],
                                          targetingSpec=request['targeting_spec'],
                                          optimizationGoal=request['optimization_goal'],
                                          attributionSpec=request['attribution_spec'],
                                          bidStrategy=request['bid_strategy'],
                                          currency=request['currency'],
                                          accessTokenFacebook=token)
    url = url.replace(' ', '').replace("'", '"')

    # Get FB delivery estimates

    facebookGraphApiResponse = requests.get(url)
    facebookGraphApiResponse = facebookGraphApiResponse.json()

    response = None
    try:
        if 'data' in facebookGraphApiResponse.keys():
            facebookGraphApiResponse = facebookGraphApiResponse['data'][0]

        # Find reach and actions bounds
        response = _EstimateDeliveryResults(facebookGraphApiResponse['daily_outcomes_curve'],
                                            facebookGraphApiResponse['estimate_dau'],
                                            facebookGraphApiResponse['estimate_mau'],
                                            request['budget'])
    except Exception as e:
        if isinstance(e, KeyError) and response and 'error_user_msg' in response['error'].keys():
            response = {
                'message': response['error']['message'],
                'error_usr_message': response['error']['error_user_msg'],
                'error_user_title': response['error']['error_user_title']}
        if isinstance(e, KeyError) and response and 'error_user_msg' not in response['error'].keys():
            response = {
                'message': response['error']['message'],
                'error_usr_message': 'An unknown error has accured; %s. Please try again or contact support.' %
                                     response['error']['message'],
                'error_user_title': 'Unknown error'}
        elif isinstance(e, KeyError) and not response:
            response = {
                'message': 'An unknown error has accured. %s. Please try again or contact support.' % str(e),
                'error_usr_message': 'An unknown error has accured. Please try again or contact support.',
                'error_user_title': 'Unknown error'
            }
        else:
            response = {
                'message': 'An unknown error has accured. Please try again or contact support.',
                'error_usr_message': 'An unknown error has accured. Please try again or contact support.',
                'error_user_title': 'Unknown error'
            }

    return response
