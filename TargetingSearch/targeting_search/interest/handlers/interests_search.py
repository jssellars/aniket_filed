import requests

from app_config.app_config import FACEBOOK_CONFIG
from app_config.app_config import FACEBOOK_SEARCH_URL, SUGGEST_INTEREST_URL
from tools.business_owner_facebook_token import get_user_token


def search_interests(search_input=None):
    if search_input is None:
        search_input = ''

    # Get user token
    token = get_user_token(FACEBOOK_CONFIG['business_owner_facebook_id'])

    # Create search url
    url = FACEBOOK_SEARCH_URL.format(api_version=FACEBOOK_CONFIG['api_version'],
                                     ad_account_id=FACEBOOK_CONFIG['ad_account_id'],
                                     search_input=search_input,
                                     token=token)
    # Run search on FB   
    results = requests.get(url).json()['data']
    for index, _ in enumerate(results):
        results[index]['key'] = results[index]['id']

    return results


def suggest_interests(interests):
    if isinstance(interests, str):
        interests = [i.title() for i in interests.split(',')]

    token = get_user_token(FACEBOOK_CONFIG['business_owner_facebook_id'])

    url = SUGGEST_INTEREST_URL.format(api_version=FACEBOOK_CONFIG['api_version'],
                                      interests=interests,
                                      token=token)
    results = requests.get(url).json()['data']
    for index, _ in enumerate(results):
        results[index]['key'] = results[index]['id']

    return results
