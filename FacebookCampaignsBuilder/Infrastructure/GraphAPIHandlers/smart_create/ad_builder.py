from typing import Dict

import requests
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adcreativelinkdata import AdCreativeLinkData
from facebook_business.adobjects.adcreativelinkdatachildattachment import (
    AdCreativeLinkDataChildAttachment as AdCreativeLDCA,
)
from facebook_business.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
from facebook_business.adobjects.adimage import AdImage

from Core.facebook.sdk_adapter.ad_objects.ad_campaign_delivery_estimate import OptimizationGoal
from Core.facebook.sdk_adapter.ad_objects.ad_creative import CallToActionType
from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPIAdPreviewBuilderHandler import FiledAdFormatEnum


def build_ads(ad_account_id: str, step_two: Dict, step_three: Dict, objective: str = None):
    ads = []
    ad_creative_facebook_id = get_ad_creative_id(int(step_three["ad_format_type"]),
                                                 ad_account_id,
                                                 step_two,
                                                 step_three,
                                                 objective)

    adverts = {
        Ad.Field.name: step_three["ad_name"],
        Ad.Field.creative: {"creative_id": ad_creative_facebook_id},
        Ad.Field.status: Ad.Status.paused,
        Ad.Field.effective_status: Ad.EffectiveStatus.paused,
        Ad.Field.tracking_specs: step_three.get("tracking_spec", None),
    }

    ads.append(adverts)
    return ads


def get_ad_creative_id(ad_creative_type: int, ad_account_id: str, step_two: Dict, step_three: Dict, objective: str):
    ad_creative_facebook_id = None
    ad_account = AdAccount(ad_account_id)
    if "adverts" not in step_three:
        return

    if ad_creative_type == FiledAdFormatEnum.IMAGE.value:
        ad_creative_facebook_id = build_image_ad_creative(step_two, step_three["adverts"], ad_account, objective)
    elif ad_creative_type == FiledAdFormatEnum.VIDEO.value:
        ad_creative_facebook_id = build_video_ad_creative(step_two, step_three["adverts"], ad_account, objective)
    elif ad_creative_type == FiledAdFormatEnum.CAROUSEL.value:
        ad_creative_facebook_id = build_carousel_ad_creative(step_two, step_three["adverts"], ad_account)

    return ad_creative_facebook_id


def build_image_ad_creative(step_two: Dict, adverts: Dict, ad_account: AdAccount, objective: str = None):
    ad_creative_link_data = build_image_link_data(ad_account, adverts, step_two.get("facebook_page_id"), objective)

    object_story_spec_data = {
        AdCreativeObjectStorySpec.Field.page_id: step_two.get("facebook_page_id", None),
        AdCreativeObjectStorySpec.Field.instagram_actor_id: step_two.get("instagram_page_id", None),
        AdCreativeObjectStorySpec.Field.link_data: ad_creative_link_data,
    }

    object_story_spec = AdCreativeObjectStorySpec()

    for k, v in object_story_spec_data.items():
        object_story_spec[k] = v

    creative_params = {
        AdCreative.Field.name: adverts.get("headline", None),
        AdCreative.Field.object_story_spec: object_story_spec,
        AdCreative.Field.link_url: adverts.get("display_link", adverts.get("deep_link", None)),
    }

    ad_creative = ad_account.create_ad_creative(params=creative_params)
    return ad_creative.get_id()


def build_video_ad_creative(
    step_two: Dict,
    adverts: Dict,
    ad_account: AdAccount,
    objective: str = None
):
    # Upload video on FB
    # TODO: we also need to provide picture thumbnail after upload
    if "video_id" not in adverts:
        ad_video_facebook_id = build_ad_video(ad_account, adverts["media_url"])
    else:
        ad_video_facebook_id = adverts["video_id"]

    call_to_action = {
        "type": adverts["call_to_action"]["value"],
        "value": {"link": adverts["website_url"]},
    }

    ad_image = _generate_image_hash(ad_account, adverts.get("picture", None))

    video_data = {
        "call_to_action": call_to_action,
        "video_id": ad_video_facebook_id,
        "image_hash": ad_image[AdImage.Field.hash],
    }

    object_story_spec_data = {
        AdCreativeObjectStorySpec.Field.page_id: step_two.get("facebook_page_id", None),
        AdCreativeObjectStorySpec.Field.instagram_actor_id: step_two.get("instagram_page_id", None),
        AdCreativeObjectStorySpec.Field.video_data: video_data,
    }

    object_story_spec = AdCreativeObjectStorySpec()

    for k in object_story_spec_data:
        object_story_spec[k] = object_story_spec_data[k]

    creative_params = build_creative_params(ad_video_facebook_id,
                                            adverts,
                                            call_to_action,
                                            object_story_spec,
                                            step_two,
                                            objective)

    ad_creative = ad_account.create_ad_creative(params=creative_params)

    return ad_creative.get_id()


def build_creative_params(ad_video_facebook_id: str,
                          adverts: Dict,
                          call_to_action: Dict,
                          object_story_spec: AdCreativeObjectStorySpec,
                          step_two: Dict,
                          objective: str = None):
    creative_params = {
        AdCreative.Field.name: adverts.get("headline", None),
        AdCreative.Field.object_story_spec: object_story_spec,
        AdCreative.Field.video_id: ad_video_facebook_id,
        AdCreative.Field.body: adverts.get("primary_test", None),
        AdCreative.Field.link_deep_link_url: adverts.get("deep_link", None),
    }
    if {"website_url", "display_link"} <= set(adverts):
        if not adverts["website_url"] and not adverts["display_link"]:
            # If objective is not part of the request, then this is called for generating Ad Preview
            if not objective:
                object_story_spec["video_data"]["call_to_action"]["type"] = CallToActionType.LIKE_PAGE.name
                creative_params[AdCreative.Field.link_url] = f"https://www.facebook.com/{step_two['facebook_page_id']}"
            elif objective == OptimizationGoal.PAGE_LIKES.name:
                creative_params[AdCreative.Field.link_url] = f"https://www.facebook.com/{step_two['facebook_page_id']}"
        else:
            creative_params[AdCreative.Field.link_url] = adverts.get("display_link")
    else:
        creative_params[AdCreative.Field.link_url] = adverts.get("deep_link")

    return creative_params


def build_carousel_ad_creative(step_two: Dict, adverts: Dict, ad_account: AdAccount):
    ad_creative_link_data = build_ad_carousel_creative_link_data(ad_account, adverts)

    object_story_spec_data = {
        AdCreativeObjectStorySpec.Field.page_id: step_two.get("facebook_page_id", None),
        AdCreativeObjectStorySpec.Field.instagram_actor_id: step_two.get("instagram_page_id", None),
        AdCreativeObjectStorySpec.Field.link_data: ad_creative_link_data,
    }

    object_story_spec = AdCreativeObjectStorySpec()

    for k, v in list(object_story_spec_data.items()):
        object_story_spec[k] = v

    creative_params = {
        AdCreative.Field.body: adverts.get("primary_text", None),
        AdCreative.Field.object_story_spec: object_story_spec,
        AdCreative.Field.link_url: adverts.get("display_link", adverts.get("deep_link", None)),
    }

    ad_creative = ad_account.create_ad_creative(params=creative_params)

    return ad_creative.get_id()


def build_image_link_data(ad_account: AdAccount, adverts: Dict, facebook_page_id: str, objective: str = None):
    call_to_action = {
        "type": adverts["call_to_action"]["value"],
        "value": {"link": adverts["website_url"]},
    }

    ad_creative_data = {
        AdCreativeLinkData.Field.message: adverts.get("primary_text", None),
        AdCreativeLinkData.Field.caption: adverts.get("display_link", None),
        AdCreativeLinkData.Field.description: adverts.get("description", None),
        AdCreativeLinkData.Field.name: adverts.get("headline", None),
    }
    call_to_action["value"]["app_link"] = adverts.get("deep_link", None)

    if "website_url" in adverts:
        if not adverts["website_url"]:
            # If objective is not part of the request, then this is called for generating Ad Preview
            if not objective:
                ad_creative_data[AdCreativeLinkData.Field.link] = f"https://www.facebook.com/{facebook_page_id}"
                call_to_action["type"] = CallToActionType.LIKE_PAGE.name
            elif objective == OptimizationGoal.PAGE_LIKES.name:
                ad_creative_data[AdCreativeLinkData.Field.link] = f"https://www.facebook.com/{facebook_page_id}"
        else:
            ad_creative_data[AdCreativeLinkData.Field.link] = adverts.get("website_url")
    else:
        ad_creative_data[AdCreativeLinkData.Field.link] = adverts.get("deep_link")

    ad_creative_link_data = AdCreativeLinkData()

    for k, v in ad_creative_data.items():
        ad_creative_link_data[k] = v

    ad_creative_link_data[AdCreativeLinkData.Field.call_to_action] = call_to_action

    # Get image hash and attach to creative
    ad_image = _generate_image_hash(ad_account, adverts.get("media_url", None))
    ad_creative_link_data[AdCreativeLinkData.Field.image_hash] = ad_image[AdImage.Field.hash]

    return ad_creative_link_data


def build_ad_carousel_creative_link_data(ad_account: AdAccount, adverts: Dict):
    ad_creative_link_data = AdCreativeLinkData()
    ad_creative_link_data[AdCreativeLinkData.Field.child_attachments] = []

    ad_creative_data = {
        AdCreativeLinkData.Field.caption: adverts.get("see_more_display_link", None),
        AdCreativeLinkData.Field.description: adverts.get("description", None),
        AdCreativeLinkData.Field.name: adverts.get("headline", None),
        AdCreativeLinkData.Field.message: adverts.get("primary_text"),
    }

    for link in ["deep_link", "see_more_url", "website_url"]:
        if link in adverts:
            ad_creative_data[AdCreativeLinkData.Field.link] = adverts.get(link)
            break

    for k, v in list(ad_creative_data.items()):
        ad_creative_link_data[k] = v

    # Create carousel cards
    for card_number, ad_template in enumerate(adverts["cards"]):
        ad_creative_ldca = AdCreativeLDCA()

        child_attachment_data = {
            AdCreativeLDCA.Field.link: ad_template.get("website_url", ad_template.get("deep_link", None)),
            AdCreativeLDCA.Field.name: ad_template.get("headline", None),
            AdCreativeLDCA.Field.description: ad_template.get("description", None),
        }

        call_to_action = {
            "type": adverts["call_to_action"]["value"],
            "value": {"link": ad_template.get("website_url", None)},
        }

        call_to_action["value"]["app_link"] = ad_template.get("deep_link", None)

        for k, v in list(child_attachment_data.items()):
            ad_creative_ldca[k] = v

        media_type = int(ad_template["media_type"])

        if media_type == FiledAdFormatEnum.IMAGE.value:
            ad_image = _generate_image_hash(ad_account, ad_template["media_url"])
            ad_creative_ldca[AdCreativeLDCA.Field.image_hash] = ad_image[AdImage.Field.hash]
        elif media_type == FiledAdFormatEnum.VIDEO.value:
            if "video_id" in ad_template and ad_template["video_id"]:
                ad_creative_ldca[AdCreativeLDCA.Field.video_id] = ad_template["video_id"]
                ad_image = _generate_image_hash(ad_account, ad_template.get("picture", None))
                ad_creative_ldca[AdCreativeLDCA.Field.image_hash] = ad_image[AdImage.Field.hash]
            elif "media_url" in ad_template and ad_template["media_url"]:
                # TODO: Upload new video and take picture as thumbnail
                ad_video_facebook_id = build_ad_video(ad_account, adverts["media_url"])
                ad_creative_ldca[AdCreativeLDCA.Field.video_id] = ad_video_facebook_id
        else:
            raise ValueError(f"Missing media from carousel card number {card_number}")

        ad_creative_ldca[AdCreativeLDCA.Field.call_to_action] = call_to_action

        ad_creative_link_data[AdCreativeLinkData.Field.child_attachments].append(ad_creative_ldca)

    return ad_creative_link_data


def _generate_image_hash(ad_account: AdAccount, image_url: str):
    # Download image from URL
    image_file = open("adCreativeImage.jpg", "wb")
    image_file.write(requests.get(image_url).content)
    image_file.close()

    # Create AdImage
    ad_image = {AdImage.Field.filename: "adCreativeImage.jpg"}
    ad_image = ad_account.create_ad_image(params=ad_image)

    return ad_image


# TODO: this needs to be fixed by Facebook in regards to uploading a video using a Page Token
def build_ad_video(ad_account: AdAccount, media_url: str):
    params = {"file_url": media_url}
    ad_video_facebook_id = ad_account.create_ad_video(params=params)
    return ad_video_facebook_id
