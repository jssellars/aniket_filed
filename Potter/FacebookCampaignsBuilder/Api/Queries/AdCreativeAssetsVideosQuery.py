import typing

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.advideo import AdVideo

from Core.Web.FacebookGraphAPI.Tools import Tools
from Potter.FacebookCampaignsBuilder.Api.Queries.AdCreativeAssetsBaseQuery import AdCreativeAssetsBaseQuery


class AdCreativeAssetsVideosQuery(AdCreativeAssetsBaseQuery):
    __ad_videos_minimal_fields = [AdVideo.Field.id, AdVideo.Field.title,
                                  AdVideo.Field.permalink_url, AdVideo.Field.picture]
    __base_permalink_url = 'https://facebook.com'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, ad_account_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            ad_account = AdAccount(fbid=ad_account_id)
            ad_account_videos_raw = ad_account.get_ad_videos(fields=self.__ad_videos_minimal_fields)
            ad_account_videos = Tools.convert_to_json(ad_account_videos_raw)
            for index, ad_video in enumerate(ad_account_videos):
                ad_account_videos[index]['permalink_url'] = self.__base_permalink_url + \
                                                            ad_account_videos[index]['permalink_url']
        except Exception as e:
            raise e

        return ad_account_videos
