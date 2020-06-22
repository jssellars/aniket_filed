from adpreview.config import FacebookConfig
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from tools.Ad import FacebookAdBuilder

from tools.business_owner_facebook_token import get_user_token


class GenerateAdPreview(object):

    def __init__(self, businessOwnerFacebookId):
        # Get user token
        token = get_user_token(businessOwnerFacebookId)

        self.facebook_ads_api = FacebookAdsApi.init(app_id=FacebookConfig.app_id,
                                                    app_secret=FacebookConfig.app_secret,
                                                    access_token=token,
                                                    api_version=FacebookConfig.api_version)
        self._businessOwnerFacebookId = businessOwnerFacebookId

    def GeneratePreview(self, adAccountFacebookId, adTemplate, pageFacebookId, instagramFacebookId):
        ad = FacebookAdBuilder(self._businessOwnerFacebookId)
        ad.buildAdCreative(adAccountFacebookId, adTemplate, pageFacebookId, instagramFacebookId)
        adFormat = adTemplate['device_placement_position']['facebookKey']

        params = {
            'ad_format': adFormat,
            'creative': ad.adCreativeDetails,
        }

        adAccount = AdAccount(fbid=adAccountFacebookId)

        adPreview = adAccount.get_generate_previews(params=params)
        if adPreview:
            adPreview = adPreview[0].export_all_data()
            adPreview = adPreview['body']
            adPreview = adPreview.replace('scrolling="yes"', 'scrolling="no"')
        else:
            adPreview = None

        return adPreview
