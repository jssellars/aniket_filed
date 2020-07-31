import typing
from enum import Enum

import requests
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adcreativelinkdata import AdCreativeLinkData
from facebook_business.adobjects.adcreativelinkdatachildattachment import AdCreativeLinkDataChildAttachment
from facebook_business.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
from facebook_business.adobjects.adimage import AdImage

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase


class FiledAdFormatEnum(Enum):
    IMAGE = 1
    CAROUSEL = 2
    COLLECTION = 3
    SLIDESHOW = 4
    VIDEO = 5
    EXISTING_POST = 6



class GraphAPIAdPreviewBuilderHandler:
    def __init__(self, facebook_config=None, permanent_token: typing.AnyStr = None):
        self.graph_api_sdk = GraphAPISdkBase(facebook_config=facebook_config,
                                             business_owner_permanent_token=permanent_token)

        self.ad = None
        self.ad_creative_link_data = None
        self.ad_creative_facebook_id = None
        self.ad_creative_details = None

    def __build_imaged_ad_creative_link_data(self, ad_template, account_id=None):
        self.ad_creative_link_data = AdCreativeLinkData()
        if 'primary_text' in ad_template.keys():
            self.ad_creative_link_data[AdCreativeLinkData.Field.message] = ad_template['primary_text']

        if 'display_link' in ad_template.keys():
            self.ad_creative_link_data[AdCreativeLinkData.Field.caption] = ad_template['display_link']

        if 'website_url' in ad_template.keys():
            self.ad_creative_link_data[AdCreativeLinkData.Field.link] = ad_template['website_url']
        elif 'deep_link' in ad_template.keys():
            self.ad_creative_link_data[AdCreativeLinkData.Field.link] = ad_template['deep_link']

        if 'description' in ad_template.keys():
            self.ad_creative_link_data[AdCreativeLinkData.Field.description] = ad_template['description']

        if 'headline' in ad_template.keys():
            self.ad_creative_link_data[AdCreativeLinkData.Field.name] = ad_template['headline']

        call_to_action = {
            'type': ad_template['call_to_action']['value'],
            'value': {
                'link': ad_template['website_url']
            },
        }

        if 'deep_link' in ad_template.keys():
            call_to_action['value']['app_link'] = ad_template['deep_link']

        self.ad_creative_link_data[AdCreativeLinkData.Field.call_to_action] = call_to_action

        # Get image hash and attach to creative
        ad_image = self.__generate_image_hash(account_id, ad_template['media_url'])
        self.ad_creative_link_data[AdCreativeLinkData.Field.image_hash] = ad_image[AdImage.Field.hash]

    @staticmethod
    def __generate_image_hash(account_id, image_url):
        # Download image from URL
        f = open('adCreativeImage.jpg', 'wb')
        f.write(requests.get(image_url).content)
        f.close()

        # Create AdImage
        ad_image = AdImage(parent_id=account_id)
        ad_image[AdImage.Field.filename] = 'adCreativeImage.jpg'
        ad_image.remote_create()

        return ad_image

    def __build_video_ad_creative_link_data(self, ad_template, account_id=None):
        self.__build_imaged_ad_creative_link_data(ad_template, account_id)

    def __build_carousel_ad_creative_link_data(self, ad_template, account_id=None):
        self.ad_creative_link_data = AdCreativeLinkData()
        self.ad_creative_link_data[AdCreativeLinkData.Field.child_attachments] = []
        self.ad_creative_link_data[AdCreativeLinkData.Field.message] = ad_template['primary_text']

        if 'deep_link' in ad_template.keys():
            self.ad_creative_link_data[AdCreativeLinkData.Field.link] = ad_template['deep_link']
        elif 'see_more_url' in ad_template.keys():
            self.ad_creative_link_data[AdCreativeLinkData.Field.link] = ad_template['see_more_url']
        elif 'website_url' in ad_template.keys():
            self.ad_creative_link_data[AdCreativeLinkData.Field.link] = ad_template['website_url']

        if 'see_more_display_link' in ad_template.keys():
            self.ad_creative_link_data[AdCreativeLinkData.Field.caption] = ad_template['see_more_display_link']

        if 'description' in ad_template.keys():
            self.ad_creative_link_data[AdCreativeLinkData.Field.description] = ad_template['description']

        if 'headline' in ad_template.keys():
            self.ad_creative_link_data[AdCreativeLinkData.Field.name] = ad_template['headline']

        # Create carousel cards
        for card_number, ad_template_carousel_frame in enumerate(ad_template['cards']):
            ad_creative_link_data_child_attachment = AdCreativeLinkDataChildAttachment()
            if 'website_url' in ad_template_carousel_frame.keys():
                ad_creative_link_data_child_attachment[AdCreativeLinkDataChildAttachment.Field.link] = \
                    ad_template_carousel_frame['website_url']
            elif 'deep_link' in ad_template_carousel_frame.keys():
                ad_creative_link_data_child_attachment[AdCreativeLinkDataChildAttachment.Field.link] = \
                    ad_template_carousel_frame['deep_link']

            if 'headline' in ad_template_carousel_frame.keys():
                ad_creative_link_data_child_attachment[AdCreativeLinkDataChildAttachment.Field.name] = \
                    ad_template_carousel_frame['headline']

            if 'description' in ad_template_carousel_frame.keys():
                ad_creative_link_data_child_attachment[AdCreativeLinkDataChildAttachment.Field.description] = \
                    ad_template_carousel_frame['description']

            if 'video_id' in ad_template_carousel_frame.keys() and ad_template_carousel_frame['video_id']:
                ad_creative_link_data_child_attachment[AdCreativeLinkDataChildAttachment.Field.video_id] = \
                    ad_template_carousel_frame['video_id']
            elif 'media_url' in ad_template_carousel_frame.keys() and ad_template_carousel_frame['media_url']:
                # Get image hash and attach to creative
                ad_image = self.__generate_image_hash(account_id, ad_template_carousel_frame['media_url'])
                ad_creative_link_data_child_attachment[AdCreativeLinkDataChildAttachment.Field.image_hash] = \
                    ad_image[AdImage.Field.hash]
            else:
                raise ValueError('Missing media from carousel card number %s' % card_number)

            call_to_action = {
                'type': ad_template['call_to_action']['value'],
                'value': {
                    'link': ad_template_carousel_frame['website_url']
                },
            }

            if 'deep_link' in ad_template_carousel_frame.keys():
                call_to_action['value']['app_link'] = ad_template_carousel_frame['deep_link']

            ad_creative_link_data_child_attachment[AdCreativeLinkDataChildAttachment.Field.call_to_action] = \
                call_to_action

            self.ad_creative_link_data[AdCreativeLinkData.Field.child_attachments].append(
                ad_creative_link_data_child_attachment)

    def __build_image_ad_creative(self, account_id, ad_template, page_facebook_id, instagram_account_facebook_id):
        object_story_spec = AdCreativeObjectStorySpec()
        object_story_spec[AdCreativeObjectStorySpec.Field.page_id] = page_facebook_id
        if instagram_account_facebook_id:
            object_story_spec[AdCreativeObjectStorySpec.Field.instagram_actor_id] = instagram_account_facebook_id

        object_story_spec[AdCreativeObjectStorySpec.Field.link_data] = self.ad_creative_link_data

        creative = AdCreative(parent_id=account_id)
        creative[AdCreative.Field.name] = ad_template['headline']
        # creative[AdCreative.Field.image_url] = ad_template['media_url']

        creative[AdCreative.Field.object_story_spec] = object_story_spec

        if 'display_link' in ad_template.keys():
            creative[AdCreative.Field.link_url] = ad_template['display_link']
        elif 'deep_link' in ad_template.keys():
            creative[AdCreative.Field.link_deep_link_url] = ad_template['deep_link']

        self.ad_creative_details = creative
        ad_creative = creative.remote_create()
        self.ad_creative_facebook_id = ad_creative.get_id()

    @staticmethod
    def __build_ad_video(account_id, mediaUrl):
        ad_account = AdAccount(fbid=account_id)
        params = {'file_url': mediaUrl}
        ad_video_facebook_id = ad_account.create_ad_video(params=params)
        return ad_video_facebook_id

    def __build_video_ad_creative(self, account_id, ad_template, page_facebook_id, instagram_facebook_id):
        # Upload video on FB
        if not ad_template['video_id']:
            ad_video_facebook_id = self.__build_ad_video(account_id, ad_template['media_url'])
        else:
            ad_video_facebook_id = ad_template['video_id']

        object_story_spec = AdCreativeObjectStorySpec()
        object_story_spec[AdCreativeObjectStorySpec.Field.page_id] = page_facebook_id
        if instagram_facebook_id:
            object_story_spec[AdCreativeObjectStorySpec.Field.instagram_actor_id] = instagram_facebook_id

        object_story_spec[AdCreativeObjectStorySpec.Field.link_data] = self.ad_creative_link_data

        creative = AdCreative(parent_id=account_id)
        creative[AdCreative.Field.title] = ad_template['headline']
        creative[AdCreative.Field.video_id] = ad_video_facebook_id
        creative[AdCreative.Field.body] = ad_template['primary_text']
        creative[AdCreative.Field.object_story_spec] = object_story_spec

        if 'display_link' in ad_template.keys():
            creative[AdCreative.Field.link_url] = ad_template['display_link']
        elif 'deep_link' in ad_template.keys():
            creative[AdCreative.Field.link_deep_link_url] = ad_template['deep_link']

        self.ad_creative_details = creative

        ad_creative = creative.remote_create()
        self.ad_creative_facebook_id = ad_creative.get_id()

    def __build_carousel_ad_creative(self, account_id, ad_template, page_facebook_id, instagram_facebook_id):
        object_story_spec = AdCreativeObjectStorySpec()
        object_story_spec[AdCreativeObjectStorySpec.Field.page_id] = page_facebook_id
        if instagram_facebook_id:
            object_story_spec[AdCreativeObjectStorySpec.Field.instagram_actor_id] = instagram_facebook_id

        # Details for each ad (image, url, etc)
        object_story_spec[AdCreativeObjectStorySpec.Field.link_data] = self.ad_creative_link_data

        creative = AdCreative(parent_id=account_id)
        creative[AdCreative.Field.body] = ad_template['primary_text']
        creative[AdCreative.Field.object_story_spec] = object_story_spec

        if 'display_link' in ad_template.keys():
            creative[AdCreative.Field.link_url] = ad_template['display_link']
        elif 'deep_link' in ad_template.keys():
            creative[AdCreative.Field.link_deep_link_url] = ad_template['deep_link']

        self.ad_creative_details = creative

        ad_creative = creative.remote_create()
        self.ad_creative_facebook_id = ad_creative.get_id()

    def build_ad_creative(self, account_id, ad_template, page_facebook_id, instagram_facebook_id):
        if ad_template['ad_format'] == FiledAdFormatEnum.IMAGE.value:
            self.__build_imaged_ad_creative_link_data(ad_template, account_id)
            self.__build_image_ad_creative(account_id, ad_template, page_facebook_id, instagram_facebook_id)
        elif ad_template['ad_format'] == FiledAdFormatEnum.VIDEO.value:
            self.__build_video_ad_creative_link_data(ad_template, account_id)
            self.__build_video_ad_creative(account_id, ad_template, page_facebook_id, instagram_facebook_id)
        elif ad_template['ad_format'] == FiledAdFormatEnum.CAROUSEL.value:
            self.__build_carousel_ad_creative_link_data(ad_template, account_id)
            self.__build_carousel_ad_creative(account_id, ad_template, page_facebook_id, instagram_facebook_id)
        # TODO : build existing post ad creative
