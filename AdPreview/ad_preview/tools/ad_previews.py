from adpreview.config import FacebookConfig
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adcreativelinkdata import AdCreativeLinkData
from facebook_business.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
from facebook_business.api import FacebookAdsApi
from tools.business_owner_facebook_token import get_user_token


class GenerateAdPreview(object):

    def __init__(self, business_owner_facebook_id):

        # Get user token
        token = get_user_token(business_owner_facebook_id)

        self.facebook_ads_api = FacebookAdsApi.init(app_id=FacebookConfig.app_id,
                                                    app_secret=FacebookConfig.app_secret,
                                                    access_token=token,
                                                    api_version=FacebookConfig.api_version)
        self._ad_account_id = None
        self._page_id = None
        self._ad_account = None
        self.story = AdCreativeObjectStorySpec()
        self.link_data = AdCreativeLinkData()
        self.creative = AdCreative()

    def create_link_data(self, data):
        params = {}
        for key, value in data.items():
            if hasattr(AdCreativeLinkData.Field, key):
                params[getattr(AdCreativeLinkData.Field, key)] = value
        self.link_data.update(params)

    def update_story_spec(self, page_id):
        self.story.update({
            AdCreativeObjectStorySpec.Field.link_data: self.link_data,
            AdCreativeObjectStorySpec.Field.page_id: page_id,
        })

    def update_creative(self):
        self.creative.update({
            AdCreative.Field.object_story_spec: self.story,
        })

    def generate_preview(self, ad_account_id, page_id, data):
        self.create_link_data(data)
        self.update_story_spec(page_id)
        self.update_creative()

        params = {
            'ad_format': data['ad_format'],
            'creative': self.creative.export_data(),
        }

        ad_account = AdAccount(fbid=ad_account_id)

        ad_preview = ad_account.get_generate_previews(params=params)
        if ad_preview:
            ad_preview = ad_preview[0].export_all_data()
            ad_preview = ad_preview['body']

            # Change scrolling from 'yes' to 'no'
            # TODO: FIND BETTER METHOD FOR REMOVING SCROLLING
            # ----- HACK ----- #
            ad_preview = ad_preview.replace('scrolling="yes"', 'scrolling="no"')
            # ----- END OF HACK ----- #

        else:
            ad_preview = None

        return ad_preview
