from facebook_business.adobjects.targetingsearch import TargetingSearch
from facebook_business.api import FacebookAdsApi

from tools.business_owner_facebook_token import get_user_token


class BaseFacebookWorker(object):

    def __init__(self, business_owner_facebook_id=None, facebook_config=None):
        assert business_owner_facebook_id is not None
        assert facebook_config is not None

        self._facebook_config = facebook_config

        token = get_user_token(business_owner_facebook_id=business_owner_facebook_id)
        self._facebook_ads_api = FacebookAdsApi.init(app_id=self._facebook_config['app_id'],
                                                     app_secret=self._facebook_config['app_secret'],
                                                     access_token=token,
                                                     api_version=self._facebook_config['api_version'])

    @staticmethod
    def _facebook_results_to_json(results):
        results_json = []
        for result in results:
            if hasattr(result, '_json'):
                results_json.append(result._json)
            else:
                results_json.append(result.export_data())

        return results_json


class FacebookLanguagesWorker(BaseFacebookWorker):

    __MAXIMUM_RESULTS_NUMBER__ = int(1e6)
    __GET_ALL_LANGUAGES_PARAMETERS__ = {
        'q': '',
        'type': 'adlocale',
        'limit': __MAXIMUM_RESULTS_NUMBER__
    }

    def get_all_values(self):
        results = TargetingSearch.search(api=self._facebook_ads_api,
                                         params=self.__GET_ALL_LANGUAGES_PARAMETERS__)

        languages = self._facebook_results_to_json(results)

        return languages


class FacebookLocationsWorker(BaseFacebookWorker):
    
    __MAXIMUM_RESULTS_NUMBER__ = int(1e6)
    __DEFAULT_GET_ALL_TYPE__ = ['country_group']
    __ALL_DATA_TYPES__ = ['country', 'country_group', 'region', 'geo_market', 'electoral_district']
    __LOCATION_SEARCH_TYPES__ = ['country', 'country_group', 'region', 'geo_market',
                                 'city', 'zip', 'electoral_district']

    def get_all_values(self):
        locations = {}
        for location_type in self.__ALL_DATA_TYPES__:
            search_results = self.search(search_type=location_type)

            locations[location_type] = search_results

        return locations

    def search(self, query_string='', search_type=None, location_types=None, limit=None):
        if isinstance(search_type, str):
            search_type = search_type.strip(' ').split(',')

        if not search_type:
            search_type = 'adgeolocation'

        if not location_types:
            location_types = self.__LOCATION_SEARCH_TYPES__

        if not limit:
            limit = self.__MAXIMUM_RESULTS_NUMBER__

        params = {
            'q': query_string,
            'type': search_type,
            'location_types': location_types,
            'limit': limit
        }

        results = TargetingSearch.search(params=params)

        results = self._facebook_results_to_json(results)

        return results


class FacebookInterestsWorker(BaseFacebookWorker):

    __MAXIMUM_RESULTS_NUMBER__ = int(1e6)

    __INTEREST_SEARCH_TYPES__ = ['adeducationschool', 'adeducationmajor', 'adinterest', 'adworkemployer',
                                 'adworkposition']

    def get_all_values(self):
        pass

    def browse_interests(self, browse_category=None):
        params = {
            'type': 'adTargetingCategory',
            'class': browse_category,
            'limit': self.__MAXIMUM_RESULTS_NUMBER__
        }

        results = TargetingSearch.search(api=self._facebook_ads_api, params=params)

        return self._facebook_results_to_json(results)

    def search_interest(self, query_string='', search_type=None):
        params = {
            'q': query_string,
            'type': search_type,
            'limit': self.__MAXIMUM_RESULTS_NUMBER__
        }

        results = TargetingSearch.search(api=self._facebook_ads_api, params=params)

        return self._facebook_results_to_json(results)

    def suggest_interests(self, source_interests=None):
        if not source_interests:
            source_interests = []

        params = {
            'interest_list': source_interests,
            'type': 'adinterestsuggestion',
            'limit': self.__MAXIMUM_RESULTS_NUMBER__
        }

        results = TargetingSearch.search(api=self._facebook_ads_api, params=params)

        return self._facebook_results_to_json(results)


