import requests
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adcreativelinkdata import AdCreativeLinkData
from facebook_business.adobjects.adcreativelinkdatachildattachment import AdCreativeLinkDataChildAttachment
from facebook_business.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
from facebook_business.adobjects.adimage import AdImage


class FiledAdFormat(object):
    video = 'Video'
    image = 'SingleImage'
    carousel = 'Carousel'


class GraphAPIAdBuilderHandler(object):

    def __init__(self):
        self.ad = None
        self.ad_creative_link_data = None
        self.ad_creative_facebook_id = None

    def _build_imaged_ad_creative_link_data(self, ad_template, ad_account_id=None):
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
        ad_image = self._generate_image_hash(ad_account_id, ad_template['media_url'])
        self.ad_creative_link_data[AdCreativeLinkData.Field.image_hash] = ad_image[AdImage.Field.hash]

    def _build_video_ad_creative_link_data(self, ad_template, ad_account_id=None):
        self._build_imaged_ad_creative_link_data(ad_template, ad_account_id)

    def _build_carousel_ad_creative_link_data(self, ad_template, ad_account_id=None):
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
                ad_image = self._generate_image_hash(ad_account_id, ad_template_carousel_frame['media_url'])
                ad_creative_link_data_child_attachment[AdCreativeLinkDataChildAttachment.Field.image_hash] = ad_image[
                    AdImage.Field.hash]
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

            ad_creative_link_data_child_attachment[AdCreativeLinkDataChildAttachment.Field.call_to_action] = call_to_action

            self.ad_creative_link_data[AdCreativeLinkData.Field.child_attachments].append(
                ad_creative_link_data_child_attachment)

    def _build_image_ad_creative(self, ad_account_id, ad_template, page_facebook_id, instagram_account_facebook_id):
        object_story_spec = AdCreativeObjectStorySpec()
        object_story_spec[AdCreativeObjectStorySpec.Field.page_id] = page_facebook_id
        if instagram_account_facebook_id:
            object_story_spec[AdCreativeObjectStorySpec.Field.instagram_actor_id] = instagram_account_facebook_id

        object_story_spec[AdCreativeObjectStorySpec.Field.link_data] = self.ad_creative_link_data

        creative = AdCreative(parent_id=ad_account_id)
        creative[AdCreative.Field.name] = ad_template['headline']
        creative[AdCreative.Field.object_story_spec] = object_story_spec

        if 'display_link' in ad_template.keys():
            creative[AdCreative.Field.link_url] = ad_template['display_link']
        elif 'deep_link' in ad_template.keys():
            creative[AdCreative.Field.link_deep_link_url] = ad_template['deep_link']

        ad_creative = creative.remote_create()

        self.ad_creative_facebook_id = ad_creative.get_id()

    @staticmethod
    def _build_ad_video(ad_account_id, media_url):
        ad_account = AdAccount(fbid=ad_account_id)
        params = {'file_url': media_url}
        ad_video_facebook_id = ad_account.create_ad_video(params=params)
        return ad_video_facebook_id

    def _build_video_ad_creative(self, ad_account_id, ad_template, page_facebook_id, instagram_facebook_id):
        # Upload video on FB
        if not ad_template['video_id']:
            ad_video_facebook_id = self._build_ad_video(ad_account_id, ad_template['media_url'])
        else:
            ad_video_facebook_id = ad_template['video_id']

        object_story_spec = AdCreativeObjectStorySpec()
        object_story_spec[AdCreativeObjectStorySpec.Field.page_id] = page_facebook_id
        if instagram_facebook_id:
            object_story_spec[AdCreativeObjectStorySpec.Field.instagram_actor_id] = instagram_facebook_id

        object_story_spec[AdCreativeObjectStorySpec.Field.link_data] = self.ad_creative_link_data

        creative = AdCreative(parent_id=ad_account_id)
        creative[AdCreative.Field.title] = ad_template['headline']
        creative[AdCreative.Field.video_id] = ad_video_facebook_id  # TODO: might need to change depending on FB response
        creative[AdCreative.Field.body] = ad_template['primary_text']
        creative[AdCreative.Field.object_story_spec] = object_story_spec

        if 'display_link' in ad_template.keys():
            creative[AdCreative.Field.link_url] = ad_template['display_link']
        elif 'deep_link' in ad_template.keys():
            creative[AdCreative.Field.link_deep_link_url] = ad_template['deep_link']

        ad_creative = creative.remote_create()

        self.ad_creative_facebook_id = ad_creative.get_id()

    def _build_carousel_ad_creative(self, ad_account_id, ad_template, page_facebook_id, instagram_facebook_id):
        object_story_spec = AdCreativeObjectStorySpec()
        object_story_spec[AdCreativeObjectStorySpec.Field.page_id] = page_facebook_id
        if instagram_facebook_id:
            object_story_spec[AdCreativeObjectStorySpec.Field.instagram_actor_id] = instagram_facebook_id

        # Details for each ad (image, url, etc)
        object_story_spec[AdCreativeObjectStorySpec.Field.link_data] = self.ad_creative_link_data

        creative = AdCreative(parent_id=ad_account_id)
        creative[AdCreative.Field.body] = ad_template['primary_text']
        creative[AdCreative.Field.object_story_spec] = object_story_spec

        if 'display_link' in ad_template.keys():
            creative[AdCreative.Field.link_url] = ad_template['display_link']
        elif 'deep_link' in ad_template.keys():
            creative[AdCreative.Field.link_deep_link_url] = ad_template['deep_link']

        ad_creative = creative.remote_create()

        self.ad_creative_facebook_id = ad_creative.get_id()

    def _build_ad_creative(self, ad_account_id, ad_template, page_facebook_id, instagram_facebook_id):
        if ad_template['ad_format'] == FiledAdFormat.image:
            self._build_imaged_ad_creative_link_data(ad_template, ad_account_id)
            self._build_image_ad_creative(ad_account_id, ad_template, page_facebook_id, instagram_facebook_id)
        elif ad_template['ad_format'] == FiledAdFormat.video:
            self._build_video_ad_creative_link_data(ad_template, ad_account_id)
            self._build_video_ad_creative(ad_account_id, ad_template, page_facebook_id, instagram_facebook_id)
        elif ad_template['ad_format'] == FiledAdFormat.carousel:
            self._build_carousel_ad_creative_link_data(ad_template, ad_account_id)
            self._build_carousel_ad_creative(ad_account_id, ad_template, page_facebook_id, instagram_facebook_id)

    def build_ad(self, ad_account_facebook_id, ad_set_facebook_id, ad_template, page_facebook_id, instagram_facebook_id):
        self._build_ad_creative(ad_account_facebook_id, ad_template, page_facebook_id, instagram_facebook_id)

        self.ad = {Ad.Field.name: 'Test Ad',
                   Ad.Field.adset_id: ad_set_facebook_id,
                   Ad.Field.creative: {'creative_id': self.ad_creative_facebook_id},
                   Ad.Field.adset: ad_set_facebook_id,
                   Ad.Field.status: Ad.Status.paused,
                   Ad.Field.effective_status: Ad.EffectiveStatus.paused}

        if 'tracking_spec' in ad_template.keys() and ad_template['tracking_spec']:
            self.ad[Ad.Field.tracking_specs] = ad_template['tracking_spec']

    @staticmethod
    def _generate_image_hash(ad_account_id, image_url):
        # Download image from URL
        image_file = open('adCreativeImage.jpg', 'wb')
        image_file.write(requests.get(image_url).content)
        image_file.close()

        # Create AdImage 
        ad_image = AdImage(parent_id=ad_account_id)
        ad_image[AdImage.Field.filename] = 'adCreativeImage.jpg'
        ad_image.remote_create()

        return ad_image
