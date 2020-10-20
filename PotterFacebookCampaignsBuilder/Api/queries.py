import typing
import urllib.parse

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.advideo import AdVideo
from facebook_business.adobjects.page import Page
from facebook_business.adobjects.pagepost import PagePost

from Core.Tools.Misc.ObjectManipulators import extract_class_attributes_values
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from PotterFacebookCampaignsBuilder.Api.catalogs import (
    special_ad_category,
    special_ad_categories,
    objectives,
    bid_strategy,
    placement,
    cta,
    ad_format,
    ad_preview_format,
    device_type,
    app_store,
)
from PotterFacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPIBudgetValidationHandler import (
    GraphAPIBudgetValidationHandler,
)
from PotterFacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPIInterestsHandler import (
    GraphAPIInterestsHandler,
)
from PotterFacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPILanguagesHandler import (
    GraphAPILanguagesHandler,
)
from PotterFacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPILocationsHandler import (
    GraphAPILocationsHandler,
)


class AdCreativeAssetsBase:
    def __init__(self, session=None, business_owner_id: typing.AnyStr = None, facebook_config=None):
        self._permanent_token = BusinessOwnerRepository(session).get_permanent_token(
            business_owner_facebook_id=business_owner_id
        )
        self._graph_api_sdk = GraphAPISdkBase(
            facebook_config=facebook_config, business_owner_permanent_token=self._permanent_token
        )


class AdCreativeAssetsImages(AdCreativeAssetsBase):
    __ad_images_minimal_fields = [AdImage.Field.id, AdImage.Field.name, AdImage.Field.permalink_url]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, ad_account_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            ad_account = AdAccount(fbid=ad_account_id)
            ad_account_images_raw = ad_account.get_ad_images(fields=self.__ad_images_minimal_fields)
            return [Tools.convert_to_json(entry) for entry in ad_account_images_raw]
        except Exception as e:
            raise e


class AdCreativeAssetsPagePosts(AdCreativeAssetsBase):
    __page_posts_minimal_fields = [PagePost.Field.id, PagePost.Field.picture, PagePost.Field.message]
    __page_posts_details_fields = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_post_details(self, page_post_facebook_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            pagePost = PagePost(fbid=page_post_facebook_id)
            pagePostRaw = pagePost.api_get(fields=self.page_posts_detail_fields)
            return Tools.convert_to_json(pagePostRaw)
        except Exception as e:
            raise e

    def get(self, page_facebook_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            page = Page(fbid=page_facebook_id)
            page_posts_raw = page.get_posts(fields=self.__page_posts_minimal_fields)
            return [Tools.convert_to_json(entry) for entry in page_posts_raw]
        except Exception as e:
            raise e

    @property
    def page_posts_detail_fields(self):
        if self.__page_posts_details_fields is None:
            self.__page_posts_details_fields = extract_class_attributes_values(PagePost.Field)

        return self.__page_posts_details_fields


class AdCreativeAssetsVideos(AdCreativeAssetsBase):
    __ad_videos_minimal_fields = [
        AdVideo.Field.id,
        AdVideo.Field.title,
        AdVideo.Field.permalink_url,
        AdVideo.Field.picture,
    ]
    __base_permalink_url = "https://facebook.com"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, ad_account_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            ad_account = AdAccount(fbid=ad_account_id)
            ad_account_videos_raw = ad_account.get_ad_videos(fields=self.__ad_videos_minimal_fields)
            ad_account_videos = [Tools.convert_to_json(entry) for entry in ad_account_videos_raw]
            for index, ad_video in enumerate(ad_account_videos):
                ad_account_videos[index]["permalink_url"] = (
                    self.__base_permalink_url + ad_account_videos[index]["permalink_url"]
                )
        except Exception as e:
            raise e

        return ad_account_videos


class BudgetValidation:
    def get(self, session=None, business_owner_id: typing.AnyStr = None, account_id: typing.AnyStr = None):
        return GraphAPIBudgetValidationHandler.handle(
            account_id=account_id,
            access_token=(
                BusinessOwnerRepository(session).get_permanent_token(business_owner_facebook_id=business_owner_id)
            ),
        )


class SmartCreateCatalogs:
    def get(self):
        classes = [
            special_ad_category.SpecialAdCategory,
            special_ad_categories.SpecialAdCategories,
            objectives.Objectives,
            bid_strategy.BidStrategy,
            placement.Placement,
            cta.CTA,
            ad_format.AdFormat,
            ad_preview_format.AdPreviewFormat,
            device_type.DeviceType,
            app_store.AppStore,
        ]
        return {class_.__name__: class_().to_json() for class_ in classes}


class TargetingSearchBase:
    def __init__(self, session=None, business_owner_id: typing.AnyStr = None, facebook_config=None):
        self._permanent_token = BusinessOwnerRepository(session).get_permanent_token(
            business_owner_facebook_id=business_owner_id
        )
        self._graph_api_sdk = GraphAPISdkBase(
            facebook_config=facebook_config, business_owner_permanent_token=self._permanent_token
        )


class TargetingSearchInterestsSearch(TargetingSearchBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def search(self, query_string: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            handler = GraphAPIInterestsHandler(graph_api_sdk=self._graph_api_sdk)
            return handler.search_interest(query_string=query_string)
        except Exception as e:
            raise e


class TargetingSearchInterestsSuggestions(TargetingSearchBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def search(self, query_string: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            source_interests = urllib.parse.unquote(query_string)
            source_interests = source_interests.replace("&", "")
            source_interests = [i.title() for i in source_interests.split(",")]

            handler = GraphAPIInterestsHandler(graph_api_sdk=self._graph_api_sdk)
            return handler.suggest_interests(source_interests=source_interests)
        except Exception as e:
            raise e


class TargetingSearchInterestsTree(TargetingSearchBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self) -> typing.List[typing.Dict]:
        try:
            handler = GraphAPIInterestsHandler(graph_api_sdk=self._graph_api_sdk)
            return handler.interests
        except Exception as e:
            raise e


class TargetingSearchLanguages(TargetingSearchBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self) -> typing.List[typing.Dict]:
        try:
            handler = GraphAPILanguagesHandler(graph_api_sdk=self._graph_api_sdk)
            return handler.get_all()
        except Exception as e:
            raise e


class TargetingSearchLocationsCountryGroups(TargetingSearchBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self) -> typing.List[typing.Dict]:
        try:
            handler = GraphAPILocationsHandler(graph_api_sdk=self._graph_api_sdk)
            return handler.get_country_groups()
        except Exception as e:
            raise e


class TargetingSearchLocationsSearch(TargetingSearchBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def search(self, query_string: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            handler = GraphAPILocationsHandler(graph_api_sdk=self._graph_api_sdk)
            return handler.search_location(query_string=query_string)
        except Exception as e:
            raise e


class TargetingSearchRegulatedInterests(TargetingSearchBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, regulated_categories: typing.List[typing.AnyStr] = None) -> typing.List[typing.Dict]:
        try:
            handler = GraphAPIInterestsHandler(graph_api_sdk=self._graph_api_sdk)
            return handler.get_regulated_interests(regulated_categories=regulated_categories)
        except Exception as e:
            raise e
