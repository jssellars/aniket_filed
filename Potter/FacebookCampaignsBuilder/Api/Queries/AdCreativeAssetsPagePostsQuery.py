import typing

from facebook_business.adobjects.page import Page
from facebook_business.adobjects.pagepost import PagePost

from Core.Tools.Misc.ObjectManipulators import extract_class_attributes_values
from Core.Web.FacebookGraphAPI.Tools import Tools
from Potter.FacebookCampaignsBuilder.Api.Queries.AdCreativeAssetsBaseQuery import AdCreativeAssetsBaseQuery


class AdCreativeAssetsPagePostsQuery(AdCreativeAssetsBaseQuery):
    __page_posts_minimal_fields = [PagePost.Field.id, PagePost.Field.picture, PagePost.Field.message]
    __page_posts_details_fields = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_post_details(self, page_post_facebook_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            pagePost = PagePost(fbid=page_post_facebook_id)
            pagePostRaw = pagePost.api_get(fields=self.page_posts_detail_fields)
            pagePost = Tools.convert_to_json(pagePostRaw)
        except Exception as e:
            raise e

        return pagePost

    def get(self, page_facebook_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            page = Page(fbid=page_facebook_id)
            page_posts_raw = page.get_posts(fields=self.__page_posts_minimal_fields)
            page_posts = Tools.convert_to_json(page_posts_raw)
        except Exception as e:
            raise e

        return page_posts

    @property
    def page_posts_detail_fields(self):
        if self.__page_posts_details_fields is None:
            self.__page_posts_details_fields = extract_class_attributes_values(PagePost.Field)

        return self.__page_posts_details_fields
