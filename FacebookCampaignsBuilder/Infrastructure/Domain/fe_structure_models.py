from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adcreativelinkdata import AdCreativeLinkData
from facebook_business.adobjects.adcreativelinkdatacalltoaction import AdCreativeLinkDataCallToAction
from facebook_business.adobjects.adcreativelinkdatacalltoactionvalue import AdCreativeLinkDataCallToActionValue
from facebook_business.adobjects.adcreativelinkdatachildattachment import AdCreativeLinkDataChildAttachment
from facebook_business.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
from facebook_business.adobjects.adcreativevideodata import AdCreativeVideoData
from facebook_business.adobjects.adpromotedobject import AdPromotedObject
from facebook_business.adobjects.conversionactionquery import ConversionActionQuery

from Core.facebook.sdk_adapter.ad_objects.ad_set import OSWithMobileDeviceGroup
from Core.Tools.Misc.FiledAdFormatEnum import FiledAdFormatEnum
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import Gender

_ad_creative = AdCreative.Field
_object_story_spec = AdCreativeObjectStorySpec.Field
_video_data = AdCreativeVideoData.Field
_link_data = AdCreativeLinkData.Field
_link_data_cta = AdCreativeLinkDataCallToAction.Field
_link_data_cta_value = AdCreativeLinkDataCallToActionValue.Field
_link_data_child_attach = AdCreativeLinkDataChildAttachment.Field
_conversion_action_query = ConversionActionQuery.Field
_promoted_object = AdPromotedObject.Field


@dataclass
class BudgetOptimization:
    amount: float
    budget_allocated_type_id: int


@dataclass
class Interest:
    id: str
    name: str
    path: List[str]

    audience_size: Optional[int] = 0
    description: Optional[str] = None
    topic: Optional[str] = None
    disambiguation_category: Optional[str] = None


@dataclass
class ImageAdvert:
    media_url: str
    primary_text: str
    headline: str
    description: str
    website_url: str

    # TODO: CTA in FE it's nested, need to discuss
    call_to_action: str
    display_link: str

    media_type: int = 1


@dataclass
class VideoAdvert:
    media_url: str
    primary_text: str
    headline: str
    website_url: str
    call_to_action: str
    display_link: str
    video_id: str

    description: Optional[str] = None
    media_type: int = 5


@dataclass
class CarouselAdvert:
    cards: List[Union[ImageAdvert, VideoAdvert]]
    media_type: int = 2


@dataclass
class TrackingSpecs:
    action_type: str
    fb_pixel: Optional[str] = None
    application: Optional[str] = None


@dataclass
class CreateAds:
    name: str
    creative: dict
    status: str
    effective_status: str
    tracking_specs: Optional[List[TrackingSpecs]] = None

    @classmethod
    def build_ad_param(cls, name: str, creative: dict, status: str, effective_status: str, request: dict):
        tracking_specs = cls.get_tracking_specs(request)
        return cls(
            name=name,
            creative=creative,
            status=status,
            effective_status=effective_status,
            tracking_specs=tracking_specs,
        )

    @classmethod
    def get_tracking_specs(cls, request):
        # Actions prepended by app_custom_event come from mobile app events and actions
        # prepended by offsite_conversion come from the Facebook Pixel.
        # Source: https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/
        tracking_specs = []
        pixel_id = request.get("pixel_id")
        pixel_app_event_id = request.get("pixel_app_event_id")

        if pixel_id:
            tracking_specs.append(
                TrackingSpecs(
                    action_type="offsite_conversion",
                    fb_pixel=pixel_id,
                )
            )

        if pixel_app_event_id:
            tracking_specs.append(
                TrackingSpecs(
                    action_type="app_custom_event",
                    application=pixel_app_event_id,
                )
            )

        return tracking_specs


@dataclass
class Ad:
    id: str
    name: str
    status: int

    ad_format_type: Optional[int] = None
    facebook_page_id: Optional[str] = None
    instagram_page_id: Optional[str] = None

    advert: Union[ImageAdvert, VideoAdvert, CarouselAdvert] = None
    post_id: Optional[str] = None
    pixel_id: Optional[str] = None
    pixel_app_event_id: Optional[str] = None

    @classmethod
    def from_ad_details(
        cls, id: str, name: str, status: int, ad_creative_data: Dict, tracking_specs: List[Dict[str, List[str]]]
    ):
        params = {}

        if _ad_creative.object_story_spec in ad_creative_data:
            object_story_spec = ad_creative_data[_ad_creative.object_story_spec]
            params["advert"] = cls.__build_advert(ad_creative_data, object_story_spec)
            params["facebook_page_id"] = object_story_spec.get(_object_story_spec.page_id)
            params["instagram_page_id"] = object_story_spec.get(_object_story_spec.instagram_actor_id)
            params["ad_format_type"] = params["advert"].media_type if params.get("advert") else None
        else:
            params["post_id"] = ad_creative_data.get(_ad_creative.object_story_id)
            params["ad_format_type"] = FiledAdFormatEnum.EXISTING_POST.value

        for tracking_spec in tracking_specs:
            if _conversion_action_query.fb_pixel in tracking_spec:
                params["pixel_id"] = tracking_spec[_conversion_action_query.fb_pixel][0]
            elif _conversion_action_query.application in tracking_spec:
                params["pixel_app_event_id"] = tracking_spec[_conversion_action_query.application][0]

        return cls(id=id, name=name, status=status, **params)

    @classmethod
    def __build_advert(cls, ad_creative_data, object_story_spec):
        if _object_story_spec.video_data in object_story_spec:
            video_data = object_story_spec[_object_story_spec.video_data]
            call_to_action = video_data.get(_video_data.call_to_action)
            cta_value = call_to_action.get(_link_data_cta.value, {})
            website_url = cta_value.get(_link_data_cta_value.link)
            display_link = cta_value.get(_link_data_cta_value.link_caption)

            advert = VideoAdvert(
                primary_text=video_data.get(_video_data.message),
                display_link=display_link,
                website_url=website_url,
                headline=video_data.get(_video_data.title),
                call_to_action=call_to_action.get(_link_data_cta.type),
                media_url=video_data.get(_video_data.image_url),
                video_id=video_data.get(_video_data.video_id),
            )

            return advert

        link_data = object_story_spec.get(_object_story_spec.link_data)
        if not link_data:
            return {}
        if _link_data.child_attachments in link_data:
            cards = []
            for child_attachment in link_data[_link_data.child_attachments]:
                if _link_data_child_attach.video_id in child_attachment:
                    card = VideoAdvert(
                        primary_text=link_data.get(_link_data.message),
                        display_link=child_attachment.get(_link_data_child_attach.caption),
                        website_url=child_attachment.get(_link_data_child_attach.link),
                        description=child_attachment.get(_link_data_child_attach.description),
                        headline=child_attachment.get(_link_data_child_attach.name),
                        call_to_action=child_attachment.get(_link_data_child_attach.call_to_action, {}).get(
                            _link_data_cta.value
                        ),
                        media_url=child_attachment.get(_link_data_child_attach.picture),
                        video_id=child_attachment[_link_data_child_attach.video_id],
                    )
                else:
                    card = ImageAdvert(
                        primary_text=link_data.get(_link_data.message),
                        display_link=child_attachment.get(_link_data_child_attach.caption),
                        website_url=child_attachment.get(_link_data_child_attach.link),
                        description=child_attachment.get(_link_data_child_attach.description),
                        headline=child_attachment.get(_link_data_child_attach.name),
                        call_to_action=child_attachment.get(_link_data_child_attach.call_to_action, {}).get(
                            _link_data_cta.value
                        ),
                        media_url=child_attachment.get(_link_data_child_attach.picture),
                    )

                cards.append(card)

            advert = CarouselAdvert(cards)

        else:
            advert = ImageAdvert(
                primary_text=link_data.get(_link_data.message),
                display_link=link_data.get(_link_data.caption),
                website_url=link_data.get(_link_data.link),
                description=link_data.get(_link_data.description),
                headline=link_data.get(_link_data.name),
                call_to_action=link_data.get(_link_data.call_to_action, {}).get(_link_data_cta.type),
                media_url=ad_creative_data.get(_ad_creative.image_url),
            )

        return advert


@dataclass
class AdSet:
    id: str
    name: str
    status: int
    destination_type: str

    optimization_goal: str
    billing_event: str

    publisher_platforms: List[str]

    min_age: int
    max_age: int

    start_time: str
    bid_control: Optional[float] = None

    page_id: Optional[str] = None
    pixel_id: Optional[str] = None
    custom_event_type: Optional[str] = None

    interests: Optional[List[Interest]] = field(default_factory=list)
    excluded_interests: Optional[List[Interest]] = field(default_factory=list)
    narrow_interests: Optional[List[Interest]] = field(default_factory=list)
    gender: Optional[int] = Gender.ALL.value
    locations: Optional[List[Dict]] = field(default_factory=list)
    languages: Optional[List[Dict]] = field(default_factory=list)
    custom_audiences: Optional[List[str]] = field(default_factory=list)
    excluded_custom_audiences: Optional[List[str]] = field(default_factory=list)

    facebook_positions: Optional[List[str]] = field(default_factory=list)
    instagram_positions: Optional[List[str]] = field(default_factory=list)
    audience_network_positions: Optional[List[str]] = field(default_factory=list)

    device_platforms: Optional[List[str]] = field(default_factory=list)
    mobile_os: Optional[str] = OSWithMobileDeviceGroup.ALL.name
    mobile_devices: Optional[List[str]] = field(default_factory=list)

    end_time: Optional[str] = None
    adset_budget_optimization: Optional[BudgetOptimization] = None
    ads: Optional[List[Ad]] = field(default_factory=list)

    def set_budget_opt(self, daily_budget, lifetime_budget):
        if lifetime_budget is not None and lifetime_budget is not "0":
            self.adset_budget_optimization = BudgetOptimization(
                amount=float(lifetime_budget) / 100, budget_allocated_type_id=0
            )
        elif daily_budget is not None and daily_budget is not "0":
            self.adset_budget_optimization = BudgetOptimization(
                amount=float(daily_budget) / 100, budget_allocated_type_id=1
            )

    def set_mobile_fields(self, user_os, user_device):
        if user_os:
            android = OSWithMobileDeviceGroup.ANDROID
            ios = OSWithMobileDeviceGroup.IOS
            if android.value.name_sdk in user_os:
                self.mobile_os = android.name
                if not user_device:
                    # default to all options checked
                    self.mobile_devices = [device.name for device in OSWithMobileDeviceGroup.ANDROID.value.items]
                else:
                    for device in user_device:
                        for android_device in OSWithMobileDeviceGroup.ANDROID.value.items:
                            if device == android_device.name_sdk:
                                self.mobile_devices.append(android_device.name)

            elif ios.value.name_sdk in user_os:
                self.mobile_os = ios.name

                if not user_device:
                    # default to all options checked
                    self.mobile_devices = [device.name for device in OSWithMobileDeviceGroup.IOS.value.items]

                else:
                    for device in user_device:
                        for ios_device in OSWithMobileDeviceGroup.IOS.value.items:
                            if device == ios_device.name_sdk:
                                self.mobile_devices.append(ios_device.name)

    def set_promoted_object_fields(self, promoted_object):
        if _promoted_object.page_id in promoted_object:
            self.page_id = promoted_object[_promoted_object.page_id]

        elif _promoted_object.pixel_id in promoted_object:
            self.pixel_id = promoted_object[_promoted_object.pixel_id]

            if _promoted_object.custom_event_type in promoted_object:
                self.custom_event_type = promoted_object[_promoted_object.custom_event_type]


@dataclass
class Campaign:
    id: str
    name: str
    status: int
    objective: str
    special_ad_category: str
    buying_type: str
    bid_strategy: Optional[str] = None  # TODO: this can be moved to CBO field, discuss with FE
    campaign_budget_optimization: Optional[BudgetOptimization] = None
    adsets: Optional[List[AdSet]] = field(default_factory=list)

    def set_budget_opt(self, daily_budget, lifetime_budget):

        if lifetime_budget:
            self.campaign_budget_optimization = BudgetOptimization(
                amount=float(lifetime_budget) / 100, budget_allocated_type_id=0
            )
        elif daily_budget:
            self.campaign_budget_optimization = BudgetOptimization(
                amount=float(daily_budget) / 100, budget_allocated_type_id=1
            )
