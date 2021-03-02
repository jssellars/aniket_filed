import urllib.parse
from dataclasses import asdict
from typing import Dict, List

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.advideo import AdVideo
from facebook_business.adobjects.page import Page
from facebook_business.adobjects.pagepost import PagePost

from Core.Tools.Misc.ObjectManipulators import extract_class_attributes_values
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.facebook.sdk_adapter.validations import JOINT_CATS
from Core.settings_models import Model
from FacebookCampaignsBuilder.Api.startup import config, fixtures
from FacebookCampaignsBuilder.Api.catalogs import (
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
    location_type,
    applink_treatment,
    action_attribution_windows,
    buying_type,
    billing_event,
    optimization_goal,
)
from FacebookCampaignsBuilder.Api.cats import CATS
from Core.Web.FacebookGraphAPI.GraphAPIHandlers.GraphAPIBudgetValidationHandler import (
    GraphAPIBudgetValidationHandler,
)
from Core.Web.FacebookGraphAPI.search import (
    GraphAPILocationsHandler,
    GraphAPILanguagesHandler, GraphAPIInterestsHandler,
)


class AdCreativeAssetsBase:
    def __init__(self, business_owner_id: str = None):
        self._permanent_token = fixtures.business_owner_repository.get_permanent_token(
            business_owner_facebook_id=business_owner_id
        )
        self._graph_api_sdk = GraphAPISdkBase(
            facebook_config=config.facebook, business_owner_permanent_token=self._permanent_token
        )


class AdCreativeAssetsImages(AdCreativeAssetsBase):
    __ad_images_minimal_fields = [
        AdImage.Field.id,
        AdImage.Field.name,
        AdImage.Field.permalink_url,
        AdImage.Field.height,
        AdImage.Field.width,
    ]

    # The choice of largest minimum dimension is based on this doc: https://www.facebook.com/business/ads-guide/image
    # Additional check for aspect ratio (width:height) is based on Facebook Instagram Feed placement
    MINIMUM_IMAGE_DIMENSION = 600
    MINIMUM_ASPECT_RATIO = 4 / 5
    MAXIMUM_ASPECT_RATIO = 191 / 100

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, ad_account_id: str = None) -> List[Dict]:
        try:
            ad_account = AdAccount(fbid=ad_account_id)
            ad_account_images_raw = ad_account.get_ad_images(fields=self.__ad_images_minimal_fields)
            ad_images_json = (Tools.convert_to_json(entry) for entry in ad_account_images_raw)
            return [image for image in ad_images_json if self.is_valid_image(image)]

        except Exception as e:
            raise e

    def is_valid_image(self, image: Dict):
        return (
            image["width"] >= self.MINIMUM_IMAGE_DIMENSION and image["height"] >= self.MINIMUM_IMAGE_DIMENSION
        ) and self.MAXIMUM_ASPECT_RATIO >= (image["width"] / image["height"]) >= self.MINIMUM_ASPECT_RATIO


class AdCreativeAssetsPagePosts(AdCreativeAssetsBase):
    __page_posts_minimal_fields = [
        PagePost.Field.id,
        PagePost.Field.picture,
        PagePost.Field.message,
        PagePost.Field.permalink_url,
        PagePost.Field.call_to_action,
    ]
    __page_posts_details_fields = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_post_details(self, page_post_facebook_id: str = None) -> List[Dict]:
        try:
            pagePost = PagePost(fbid=page_post_facebook_id)
            pagePostRaw = pagePost.api_get(fields=self.page_posts_detail_fields)
            return Tools.convert_to_json(pagePostRaw)
        except Exception as e:
            raise e

    def get(self, page_facebook_id: str = None) -> List[Dict]:
        try:
            page = Page(fbid=page_facebook_id)
            page_posts_raw = page.get_posts(fields=self.__page_posts_minimal_fields)
            result = [Tools.convert_to_json(entry) for entry in page_posts_raw]
            for entry in result:
                entry["primary_text"] = entry.pop("message", None)
                call_to_action = entry.get("call_to_action")
                if call_to_action:
                    call_to_action["value"] = call_to_action.pop("type")

            return result

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
        AdVideo.Field.is_instagram_eligible,
    ]
    __base_permalink_url = "https://facebook.com"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, ad_account_id: str = None, is_instagram_eligible: bool = False) -> List[Dict]:
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

        return (
            ad_account_videos
            if not is_instagram_eligible
            else [video for video in ad_account_videos if video["is_instagram_eligible"]]
        )


class BudgetValidation:
    @staticmethod
    def get(business_owner_id: str = None, account_id: str = None):
        return GraphAPIBudgetValidationHandler.handle(
            account_id,
            fixtures.business_owner_repository.get_permanent_token(business_owner_facebook_id=business_owner_id),
            config,
        )


class SmartCreateCats:
    def get(self):
        result = {c.__name__: c.as_dict() for c in CATS}
        result.update(validations={k: asdict(v) for k, v in JOINT_CATS.items()})

        return result


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
            location_type.LocationType,
            location_type.LocationTypeGroup,
            applink_treatment.ApplinkTreatment,
            action_attribution_windows.ActionAttributionWindows,
            buying_type.BuyingType,
            billing_event.BillingEvent,
            optimization_goal.OptimizationGoal,
            optimization_goal.OptimizationGoalWithBillingEvents,
        ]

        return {class_.__name__: class_().to_json() for class_ in classes}


class TargetingSearchBase:
    def __init__(self, business_owner_id: str = None):
        self._permanent_token = fixtures.business_owner_repository.get_permanent_token(
            business_owner_facebook_id=business_owner_id
        )
        self._graph_api_sdk = GraphAPISdkBase(
            facebook_config=config.facebook, business_owner_permanent_token=self._permanent_token
        )


class TargetingSearchInterestsSearch(TargetingSearchBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def search(self, query_string: str = None) -> List[Dict]:
        try:
            handler = GraphAPIInterestsHandler(graph_api_sdk=self._graph_api_sdk)
            return handler.search_interest(query_string=query_string)
        except Exception as e:
            raise e


class TargetingSearchInterestsSuggestions(TargetingSearchBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def search(self, query_string: str = None) -> List[Dict]:
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

    def get(self) -> List[Dict]:
        try:
            handler = GraphAPIInterestsHandler(graph_api_sdk=self._graph_api_sdk)
            return handler.interests
        except Exception as e:
            raise e


class TargetingSearchLanguages(TargetingSearchBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self) -> List[Dict]:
        try:
            handler = GraphAPILanguagesHandler(graph_api_sdk=self._graph_api_sdk)
            return handler.get_all()
        except Exception as e:
            raise e


class TargetingSearchLocationsCountryGroups(TargetingSearchBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self) -> List[Dict]:
        try:
            handler = GraphAPILocationsHandler(graph_api_sdk=self._graph_api_sdk)
            return handler.get_country_groups()
        except Exception as e:
            raise e


class TargetingSearchLocationsSearch(TargetingSearchBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def search(self, query_string: str = None) -> List[Dict]:
        try:
            handler = GraphAPILocationsHandler(graph_api_sdk=self._graph_api_sdk)
            return handler.search_location(query_string=query_string)
        except Exception as e:
            raise e


class TargetingSearchRegulatedInterests(TargetingSearchBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, regulated_categories: List[str] = None) -> List[Dict]:
        try:
            handler = GraphAPIInterestsHandler(graph_api_sdk=self._graph_api_sdk)
            return handler.get_regulated_interests(regulated_categories=regulated_categories)
        except Exception as e:
            raise e


def get_account_advertisable_apps(ad_account_id: str, permanent_token: str, config: Model):
    GraphAPISdkBase(facebook_config=config.facebook, business_owner_permanent_token=permanent_token)
    ad_account = AdAccount(ad_account_id)
    apps = ad_account.get_advertisable_applications()

    return [entry.export_all_data() for entry in apps]
