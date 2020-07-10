import requests
from adpreview.config import FacebookConfig
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adcreativelinkdata import AdCreativeLinkData
from facebook_business.adobjects.adcreativelinkdatachildattachment import AdCreativeLinkDataChildAttachment
from facebook_business.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
from facebook_business.adobjects.adimage import AdImage
from facebook_business.api import FacebookAdsApi

from tools.business_owner_facebook_token import get_user_token


class FiledAdFormat(object):
    image = 1
    carousel = 2
    collection = 3
    slideshow = 4
    video = 5


class FacebookAdBuilder(object):

    def __init__(self, businessOwnerFacebookId=None):

        # Get user token
        token = get_user_token(businessOwnerFacebookId)

        self.facebookAdsAPI = FacebookAdsApi.init(app_id=FacebookConfig.app_id,
                                                  app_secret=FacebookConfig.app_secret,
                                                  access_token=token,
                                                  api_version=FacebookConfig.api_version)

        self.ad = None
        self.adCreativeLinkData = None
        self.adCreativeFacebookId = None
        self.adCreativeDetails = None

    def _buildImagedAdCreativeLinkData(self, adTemplate, adAccountId=None):
        self.adCreativeLinkData = AdCreativeLinkData()
        if 'primary_text' in adTemplate.keys():
            self.adCreativeLinkData[AdCreativeLinkData.Field.message] = adTemplate['primary_text']

        if 'display_link' in adTemplate.keys():
            self.adCreativeLinkData[AdCreativeLinkData.Field.caption] = adTemplate['display_link']

        if 'website_url' in adTemplate.keys():
            self.adCreativeLinkData[AdCreativeLinkData.Field.link] = adTemplate['website_url']
        elif 'deep_link' in adTemplate.keys():
            self.adCreativeLinkData[AdCreativeLinkData.Field.link] = adTemplate['deep_link']

        if 'description' in adTemplate.keys():
            self.adCreativeLinkData[AdCreativeLinkData.Field.description] = adTemplate['description']

        if 'headline' in adTemplate.keys():
            self.adCreativeLinkData[AdCreativeLinkData.Field.name] = adTemplate['headline']

        call_to_action = {
            'type': adTemplate['call_to_action']['value'],
            'value': {
                'link': adTemplate['website_url']
            },
        }

        if 'deep_link' in adTemplate.keys():
            call_to_action['value']['app_link'] = adTemplate['deep_link']

        self.adCreativeLinkData[AdCreativeLinkData.Field.call_to_action] = call_to_action

        # Get image hash and attach to creative
        adImage = self._GenerateImageHash(adAccountId, adTemplate['media_url'])
        self.adCreativeLinkData[AdCreativeLinkData.Field.image_hash] = adImage[AdImage.Field.hash]

    @staticmethod
    def _GenerateImageHash(adAccountId, imageUrl):
        # Download image from URL
        f = open('adCreativeImage.jpg', 'wb')
        f.write(requests.get(imageUrl).content)
        f.close()

        # Create AdImage 
        adImage = AdImage(parent_id=adAccountId)
        adImage[AdImage.Field.filename] = 'adCreativeImage.jpg'
        adImage.remote_create()

        return adImage

    def _buildVideoAdCreativeLinkData(self, adTemplate, adAccountId=None):
        self._buildImagedAdCreativeLinkData(adTemplate, adAccountId)

    def _buildCarouselAdCreativeLinkData(self, adTemplate, adAccountId=None):
        self.adCreativeLinkData = AdCreativeLinkData()
        self.adCreativeLinkData[AdCreativeLinkData.Field.child_attachments] = []
        self.adCreativeLinkData[AdCreativeLinkData.Field.message] = adTemplate['primary_text']

        if 'deep_link' in adTemplate.keys():
            self.adCreativeLinkData[AdCreativeLinkData.Field.link] = adTemplate['deep_link']
        elif 'see_more_url' in adTemplate.keys():
            self.adCreativeLinkData[AdCreativeLinkData.Field.link] = adTemplate['see_more_url']
        elif 'website_url' in adTemplate.keys():
            self.adCreativeLinkData[AdCreativeLinkData.Field.link] = adTemplate['website_url']

        if 'see_more_display_link' in adTemplate.keys():
            self.adCreativeLinkData[AdCreativeLinkData.Field.caption] = adTemplate['see_more_display_link']

        if 'description' in adTemplate.keys():
            self.adCreativeLinkData[AdCreativeLinkData.Field.description] = adTemplate['description']

        if 'headline' in adTemplate.keys():
            self.adCreativeLinkData[AdCreativeLinkData.Field.name] = adTemplate['headline']

        # Create carousel cards
        for cardNumber, adTemplateCarouselFrame in enumerate(adTemplate['cards']):
            adCreativeLinkDataChildAttachment = AdCreativeLinkDataChildAttachment()
            if 'website_url' in adTemplateCarouselFrame.keys():
                adCreativeLinkDataChildAttachment[AdCreativeLinkDataChildAttachment.Field.link] = \
                adTemplateCarouselFrame['website_url']
            elif 'deep_link' in adTemplateCarouselFrame.keys():
                adCreativeLinkDataChildAttachment[AdCreativeLinkDataChildAttachment.Field.link] = \
                adTemplateCarouselFrame['deep_link']

            if 'headline' in adTemplateCarouselFrame.keys():
                adCreativeLinkDataChildAttachment[AdCreativeLinkDataChildAttachment.Field.name] = \
                adTemplateCarouselFrame['headline']

            if 'description' in adTemplateCarouselFrame.keys():
                adCreativeLinkDataChildAttachment[AdCreativeLinkDataChildAttachment.Field.description] = \
                adTemplateCarouselFrame['description']

            if 'video_id' in adTemplateCarouselFrame.keys() and adTemplateCarouselFrame['video_id']:
                adCreativeLinkDataChildAttachment[AdCreativeLinkDataChildAttachment.Field.video_id] = \
                adTemplateCarouselFrame['video_id']
            elif 'media_url' in adTemplateCarouselFrame.keys() and adTemplateCarouselFrame['media_url']:
                # Get image hash and attach to creative
                adImage = self._GenerateImageHash(adAccountId, adTemplateCarouselFrame['media_url'])
                adCreativeLinkDataChildAttachment[AdCreativeLinkDataChildAttachment.Field.image_hash] = adImage[
                    AdImage.Field.hash]
            else:
                raise ValueError('Missing media from carousel card number %s' % cardNumber)

            call_to_action = {
                'type': adTemplate['call_to_action']['value'],
                'value': {
                    'link': adTemplateCarouselFrame['website_url']
                },
            }

            if 'deep_link' in adTemplateCarouselFrame.keys():
                call_to_action['value']['app_link'] = adTemplateCarouselFrame['deep_link']

            adCreativeLinkDataChildAttachment[AdCreativeLinkDataChildAttachment.Field.call_to_action] = call_to_action

            self.adCreativeLinkData[AdCreativeLinkData.Field.child_attachments].append(
                adCreativeLinkDataChildAttachment)

    def _buildImageAdCreative(self, adAccountId, adTemplate, pageFacebookId, instagramAccountFacebookId):
        objectStorySpec = AdCreativeObjectStorySpec()
        objectStorySpec[AdCreativeObjectStorySpec.Field.page_id] = pageFacebookId
        if instagramAccountFacebookId:
            objectStorySpec[AdCreativeObjectStorySpec.Field.instagram_actor_id] = instagramAccountFacebookId

        objectStorySpec[AdCreativeObjectStorySpec.Field.link_data] = self.adCreativeLinkData

        creative = AdCreative(parent_id=adAccountId)
        creative[AdCreative.Field.name] = adTemplate['headline']
        # creative[AdCreative.Field.image_url] = adTemplate['media_url']

        creative[AdCreative.Field.object_story_spec] = objectStorySpec

        if 'display_link' in adTemplate.keys():
            creative[AdCreative.Field.link_url] = adTemplate['display_link']
        elif 'deep_link' in adTemplate.keys():
            creative[AdCreative.Field.link_deep_link_url] = adTemplate['deep_link']

        self.adCreativeDetails = creative
        adCreative = creative.remote_create()
        self.adCreativeFacebookId = adCreative.get_id()

    @staticmethod
    def _BuildAdVideo(adAccountId, mediaUrl):
        adAccount = AdAccount(fbid=adAccountId)
        params = {'file_url': mediaUrl}
        adVideoFacebookId = adAccount.create_ad_video(params=params)
        return adVideoFacebookId

    def _buildVideoAdCreative(self, adAccountId, adTemplate, pageFacebookId, instagramFacebookId):
        # Upload video on FB
        if not adTemplate['video_id']:
            adVideoFacebookId = self._BuildAdVideo(adAccountId, adTemplate['media_url'])
        else:
            adVideoFacebookId = adTemplate['video_id']

        objectStorySpec = AdCreativeObjectStorySpec()
        objectStorySpec[AdCreativeObjectStorySpec.Field.page_id] = pageFacebookId
        if instagramFacebookId:
            objectStorySpec[AdCreativeObjectStorySpec.Field.instagram_actor_id] = instagramFacebookId

        objectStorySpec[AdCreativeObjectStorySpec.Field.link_data] = self.adCreativeLinkData

        creative = AdCreative(parent_id=adAccountId)
        creative[AdCreative.Field.title] = adTemplate['headline']
        creative[AdCreative.Field.video_id] = adVideoFacebookId
        creative[AdCreative.Field.body] = adTemplate['primary_text']
        creative[AdCreative.Field.object_story_spec] = objectStorySpec

        if 'display_link' in adTemplate.keys():
            creative[AdCreative.Field.link_url] = adTemplate['display_link']
        elif 'deep_link' in adTemplate.keys():
            creative[AdCreative.Field.link_deep_link_url] = adTemplate['deep_link']

        self.adCreativeDetails = creative

        adCreative = creative.remote_create()
        self.adCreativeFacebookId = adCreative.get_id()

    def _buildCarouselAdCreative(self, adAccountId, adTemplate, pageFacebookId, instagramFacebookId):
        objectStorySpec = AdCreativeObjectStorySpec()
        objectStorySpec[AdCreativeObjectStorySpec.Field.page_id] = pageFacebookId
        if instagramFacebookId:
            objectStorySpec[AdCreativeObjectStorySpec.Field.instagram_actor_id] = instagramFacebookId

        # Details for each ad (image, url, etc)
        objectStorySpec[AdCreativeObjectStorySpec.Field.link_data] = self.adCreativeLinkData

        creative = AdCreative(parent_id=adAccountId)
        creative[AdCreative.Field.body] = adTemplate['primary_text']
        creative[AdCreative.Field.object_story_spec] = objectStorySpec

        if 'display_link' in adTemplate.keys():
            creative[AdCreative.Field.link_url] = adTemplate['display_link']
        elif 'deep_link' in adTemplate.keys():
            creative[AdCreative.Field.link_deep_link_url] = adTemplate['deep_link']

        self.adCreativeDetails = creative

        adCreative = creative.remote_create()
        self.adCreativeFacebookId = adCreative.get_id()

    def buildAdCreative(self, adAccountId, adTemplate, pageFacebookId, instagramFacebookId):
        if adTemplate['ad_format'] == FiledAdFormat.image:
            self._buildImagedAdCreativeLinkData(adTemplate, adAccountId)
            self._buildImageAdCreative(adAccountId, adTemplate, pageFacebookId, instagramFacebookId)
        elif adTemplate['ad_format'] == FiledAdFormat.video:
            self._buildVideoAdCreativeLinkData(adTemplate, adAccountId)
            self._buildVideoAdCreative(adAccountId, adTemplate, pageFacebookId, instagramFacebookId)
        elif adTemplate['ad_format'] == FiledAdFormat.carousel:
            self._buildCarouselAdCreativeLinkData(adTemplate, adAccountId)
            self._buildCarouselAdCreative(adAccountId, adTemplate, pageFacebookId, instagramFacebookId)