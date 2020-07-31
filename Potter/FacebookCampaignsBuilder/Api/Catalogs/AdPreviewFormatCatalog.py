import copy
from facebook_business.adobjects.adpreview import AdPreview
from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport

from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogBase import CatalogBase
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from Potter.FacebookCampaignsBuilder.Api.Catalogs.AdFormatCatalog import image, video, carousel, existing_post

audience_network_instream_video = CatalogNode(AdPreview.AdFormat.audience_network_instream_video,
                                              'Apps & Sites instream video')
audience_network_instream_video_mobile = CatalogNode(AdPreview.AdFormat.audience_network_instream_video_mobile,
                                                     'Apps & Sites mobile video')
audience_network_outstream_video = CatalogNode(AdPreview.AdFormat.audience_network_outstream_video,
                                               'Apps & Sites outstream video')
audience_network_rewarded_video = CatalogNode(AdPreview.AdFormat.audience_network_rewarded_video,
                                              'Apps & Sites rewarded video')
desktop_feed_standard = CatalogNode(AdPreview.AdFormat.desktop_feed_standard,
                                    'Desktop Feed')
facebook_story_mobile = CatalogNode(AdPreview.AdFormat.facebook_story_mobile,
                                    'Facebook Story')
instagram_explore_contextual = CatalogNode(AdPreview.AdFormat.instagram_explore_contextual,
                                           'Instagram explore contextual')
instagram_explore_immersive = CatalogNode(AdPreview.AdFormat.instagram_explore_immersive,
                                          'Instagram explore immersive')
instagram_standard = CatalogNode(AdPreview.AdFormat.instagram_standard, 'Instagram standard')
instagram_story = CatalogNode(AdPreview.AdFormat.instagram_story, 'Instagram story')
instant_article_recirculation_ad = CatalogNode(AdPreview.AdFormat.instant_article_recirculation_ad,
                                               'Instant article recirculation')
instant_article_standard = CatalogNode(AdPreview.AdFormat.instant_article_standard,
                                       'Instant article standard')
instream_video_desktop = CatalogNode(AdPreview.AdFormat.instream_video_desktop,
                                     'Instream video desktop')
instream_video_mobile = CatalogNode(AdPreview.AdFormat.instream_video_mobile,
                                    'Instream video mobile')
job_browser_desktop = CatalogNode(AdPreview.AdFormat.job_browser_desktop,
                                  'Job browser desktop')
job_browser_mobile = CatalogNode(AdPreview.AdFormat.job_browser_mobile,
                                 'Job browser mobile')
marketplace_mobile = CatalogNode(AdPreview.AdFormat.marketplace_mobile,
                                 'Marketplace mobile')
messenger_mobile_inbox_media = CatalogNode(AdPreview.AdFormat.messenger_mobile_inbox_media,
                                           'Messenger mobile inbox')
messenger_mobile_story_media = CatalogNode(AdPreview.AdFormat.messenger_mobile_story_media,
                                           'Messenger mobile story')
mobile_banner = CatalogNode(AdPreview.AdFormat.mobile_banner, 'Mobile banner')
mobile_feed_basic = CatalogNode(AdPreview.AdFormat.mobile_feed_basic, 'Mobile feed basic')
mobile_feed_standard = CatalogNode(AdPreview.AdFormat.mobile_feed_standard, 'Mobile feed standard')
mobile_fullwidth = CatalogNode(AdPreview.AdFormat.mobile_fullwidth, 'Mobile fullwidth')
mobile_interstitial = CatalogNode(AdPreview.AdFormat.mobile_interstitial, 'Mobile interstitial')
mobile_medium_rectangle = CatalogNode(AdPreview.AdFormat.mobile_medium_rectangle, 'Mobile medium rectangle')
mobile_native = CatalogNode(AdPreview.AdFormat.mobile_native, 'Mobile native')
right_column_standard = CatalogNode(AdPreview.AdFormat.right_column_standard, 'Right Column Standard')
suggested_video_desktop = CatalogNode(AdPreview.AdFormat.suggested_video_desktop, 'Suggested video desktop')
suggested_video_mobile = CatalogNode(AdPreview.AdFormat.suggested_video_mobile, 'Suggested video mobile')
watch_feed_mobile = CatalogNode(AdPreview.AdFormat.watch_feed_mobile, 'Watch feed mobile')


all_facebook_formats = CatalogNode(ContentDeliveryReport.Platform.facebook, 'Facebook', None, None,
                                   [desktop_feed_standard, facebook_story_mobile, instant_article_standard,
                                    instream_video_desktop, instream_video_mobile, marketplace_mobile,
                                    mobile_feed_basic, mobile_feed_standard, right_column_standard,
                                    suggested_video_desktop, suggested_video_mobile, watch_feed_mobile])

all_instagram_formats = CatalogNode(ContentDeliveryReport.Platform.instagram, 'Instagram', None, None,
                                    [instagram_standard, instagram_story, instagram_explore_contextual,
                                     instagram_explore_immersive])

all_audience_network_formats = CatalogNode(ContentDeliveryReport.Platform.audience_network, 'Apps & Sites',
                                           None, None,
                                           [audience_network_instream_video, audience_network_instream_video_mobile,
                                            mobile_banner, mobile_fullwidth, mobile_interstitial,
                                            mobile_medium_rectangle, mobile_native])

image = copy.deepcopy(image)
image.description = None
image.image_name = None
image.children = [all_facebook_formats, all_instagram_formats, all_audience_network_formats]

video = copy.deepcopy(video)
video.description = None
video.image_name = None
video.children = [all_facebook_formats, all_instagram_formats, all_audience_network_formats]


carousel = copy.deepcopy(carousel)
carousel.description = None
carousel.image_name = None
carousel.children = [all_facebook_formats, all_instagram_formats, all_audience_network_formats]


existing_post_facebook_formats = CatalogNode(ContentDeliveryReport.Platform.facebook, 'Facebook', None, None,
                                             [right_column_standard, desktop_feed_standard, mobile_feed_standard])

existing_post_instagram_formats = CatalogNode(ContentDeliveryReport.Platform.instagram, 'Instagram', None, None,
                                              [instagram_standard])

existing_post = copy.deepcopy(existing_post)
existing_post.description = None
existing_post.image_name = None
existing_post.children = [existing_post_facebook_formats, existing_post_instagram_formats]


class AdPreviewFormatCatalog(CatalogBase):
    A_image = image
    B_video = video
    C_carousel = carousel
    D_existing_post = existing_post
