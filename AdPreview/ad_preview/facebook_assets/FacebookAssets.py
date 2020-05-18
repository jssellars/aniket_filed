from copy import deepcopy

from adpreview.config import FacebookConfig
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.page import Page
from facebook_business.adobjects.pagepost import PagePost
from facebook_business.api import FacebookAdsApi
from tools.Tools import Tools
from tools.business_owner_facebook_token import get_user_token


def _GetClassProperties(targetObject):
    properties = [f for f in dir(targetObject) if not callable(getattr(targetObject, f)) and not f.startswith('__')]

    return properties


class FacebookAssets(object):
    _adImagesMinimalFields = ['id', 'name', 'permalink_url']
    _pagePostsDetailsFields = [PagePost.Field.__dict__[v] for v in _GetClassProperties(PagePost.Field())]
    _pagePostsMinimalFields = ['id', 'picture', 'message']
    _adVideosMinimalFields = ['id', 'permalink_url', 'title']

    def __init__(self, business_owner_facebook_id):

        # Get user token
        token = get_user_token(business_owner_facebook_id)

        self.facebook_ads_api = FacebookAdsApi.init(app_id=FacebookConfig.app_id,
                                                    app_secret=FacebookConfig.app_secret,
                                                    access_token=token,
                                                    api_version=FacebookConfig.api_version)

    def GetAdImagesMinimal(self, adAccountFacebookId=None):
        assert adAccountFacebookId is not None

        try:
            adAccount = AdAccount(fbid=adAccountFacebookId)
            adAccountImagesRaw = adAccount.get_ad_images(fields=self._adImagesMinimalFields)
            adAccountImages = Tools.ConvertToJson(adAccountImagesRaw)
        except Exception as e:
            raise e

        return adAccountImages

    def GetAdVideosMinimal(self, adAccountFacebookId=None):
        assert adAccountFacebookId is not None

        try:
            adAccount = AdAccount(fbid=adAccountFacebookId)
            adVideosRaw = adAccount.get_ad_videos(fields=self._adVideosMinimalFields)
            adVideosRaw = Tools.ConvertToJson(adVideosRaw)
            adVideos = []
            for adVideo in adVideosRaw:
                adVideo['permalink_url'] = 'https://facebook.com' + adVideo['permalink_url']
                adVideos.append(deepcopy(adVideo))
        except Exception as e:
            raise e

        return adVideos

    def GetPagePostDetails(self, pagePostFacebookId=None):
        assert pagePostFacebookId is not None

        try:
            pagePost = PagePost(fbid=pagePostFacebookId)
            pagePostRaw = pagePost.api_get(fields=self._pagePostsDetailsFields)
            pagePost = Tools.ConvertToJson(pagePostRaw)
        except Exception as e:
            raise e

        return pagePost

    def GetPagePostsMinimal(self, pageFacebookId=None):
        assert pageFacebookId is not None

        try:
            page = Page(fbid=pageFacebookId)
            pagePostsRaw = page.get_posts(fields=self._pagePostsMinimalFields)
            pagePosts = Tools.ConvertToJson(pagePostsRaw)
        except Exception as e:
            raise e

        return pagePosts
