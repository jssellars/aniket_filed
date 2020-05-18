from facebook_business.api import FacebookAdsApi


class GraphAPISdkBase:

    def __init__(self, facebook_config, business_owner_permanent_token):
        self._facebookAdsApi = FacebookAdsApi.init(app_id=facebook_config.app_id,
                                                   app_secret=facebook_config.app_secret,
                                                   access_token=business_owner_permanent_token,
                                                   api_version=facebook_config.api_version)
