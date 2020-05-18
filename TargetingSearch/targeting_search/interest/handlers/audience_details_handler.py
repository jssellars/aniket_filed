import requests
from app_config.app_config import AUDIENCE_DETAILS_URL
from app_config.app_config import FACEBOOK_CONFIG
from tools.business_owner_facebook_token import get_user_token


def estimate_audiece_size(request=None):
    try:
        token = get_user_token(request['business_owner_facebook_id'])
    except KeyError:
        token = get_user_token(FACEBOOK_CONFIG["business_owner_facebook_id"])

    url = AUDIENCE_DETAILS_URL.format(api_version=request["api_version"],
                                      ad_account_id=request["ad_account_id"],
                                      targeting_spec=request["targeting_spec"],
                                      token=token,
                                      optimization_goal=request["optimization_goal"],
                                      attribution_spec=request["attribution_spec"],
                                      bid_strategy=request["bid_strategy"])
    try:
        raw_response = requests.get(url).json()
        response = {
            "estimated_dau": raw_response['data']['estimated_dau'],
            "estimated_mau": raw_response['data']['estimated_mau']
        }
    except Exception as e:
        response = e

    return response
