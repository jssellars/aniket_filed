import typing

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adimage import AdImage

from Core.Web.FacebookGraphAPI.Tools import Tools
from Potter.FacebookCampaignsBuilder.Api.Queries.AdCreativeAssetsBaseQuery import AdCreativeAssetsBaseQuery


class AdCreativeAssetsImagesQuery(AdCreativeAssetsBaseQuery):
    __ad_images_minimal_fields = [AdImage.Field.id, AdImage.Field.name, AdImage.Field.permalink_url]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, ad_account_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            ad_account = AdAccount(fbid=ad_account_id)
            ad_account_images_raw = ad_account.get_ad_images(fields=self.__ad_images_minimal_fields)
            ad_account_images = [Tools.convert_to_json(entry) for entry in ad_account_images_raw]
        except Exception as e:
            raise e

        return ad_account_images
