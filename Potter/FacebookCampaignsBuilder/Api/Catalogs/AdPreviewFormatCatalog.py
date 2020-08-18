import copy
from facebook_business.adobjects.adpreview import AdPreview
from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport

from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogBase import CatalogBase
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from Potter.FacebookCampaignsBuilder.Api.Catalogs.AdFormatCatalog import image, video, carousel, existing_post

audience_network_instream_video = CatalogNode(AdPreview.AdFormat.audience_network_instream_video)
audience_network_instream_video_mobile = CatalogNode(AdPreview.AdFormat.audience_network_instream_video_mobile)
audience_network_outstream_video = CatalogNode(AdPreview.AdFormat.audience_network_outstream_video)
audience_network_rewarded_video = CatalogNode(AdPreview.AdFormat.audience_network_rewarded_video)
desktop_feed_standard = CatalogNode(AdPreview.AdFormat.desktop_feed_standard)
facebook_story_mobile = CatalogNode(AdPreview.AdFormat.facebook_story_mobile)
instagram_explore_contextual = CatalogNode(AdPreview.AdFormat.instagram_explore_contextual)
instagram_explore_immersive = CatalogNode(AdPreview.AdFormat.instagram_explore_immersive)
instagram_standard = CatalogNode(AdPreview.AdFormat.instagram_standard)
instagram_story = CatalogNode(AdPreview.AdFormat.instagram_story)
instant_article_recirculation_ad = CatalogNode(AdPreview.AdFormat.instant_article_recirculation_ad)
instant_article_standard = CatalogNode(AdPreview.AdFormat.instant_article_standard)
instream_video_desktop = CatalogNode(AdPreview.AdFormat.instream_video_desktop)
instream_video_mobile = CatalogNode(AdPreview.AdFormat.instream_video_mobile)
job_browser_desktop = CatalogNode(AdPreview.AdFormat.job_browser_desktop)
job_browser_mobile = CatalogNode(AdPreview.AdFormat.job_browser_mobile)
marketplace_mobile = CatalogNode(AdPreview.AdFormat.marketplace_mobile)
messenger_mobile_inbox_media = CatalogNode(AdPreview.AdFormat.messenger_mobile_inbox_media)
messenger_mobile_story_media = CatalogNode(AdPreview.AdFormat.messenger_mobile_story_media)
mobile_banner = CatalogNode(AdPreview.AdFormat.mobile_banner)
mobile_feed_basic = CatalogNode(AdPreview.AdFormat.mobile_feed_basic)
mobile_feed_standard = CatalogNode(AdPreview.AdFormat.mobile_feed_standard)
mobile_fullwidth = CatalogNode(AdPreview.AdFormat.mobile_fullwidth)
mobile_interstitial = CatalogNode(AdPreview.AdFormat.mobile_interstitial)
mobile_medium_rectangle = CatalogNode(AdPreview.AdFormat.mobile_medium_rectangle)
mobile_native = CatalogNode(AdPreview.AdFormat.mobile_native)
right_column_standard = CatalogNode(AdPreview.AdFormat.right_column_standard)
suggested_video_desktop = CatalogNode(AdPreview.AdFormat.suggested_video_desktop)
suggested_video_mobile = CatalogNode(AdPreview.AdFormat.suggested_video_mobile)
watch_feed_mobile = CatalogNode(AdPreview.AdFormat.watch_feed_mobile)


all_facebook_formats = CatalogNode(ContentDeliveryReport.Platform.facebook,
                                   [desktop_feed_standard, facebook_story_mobile, instant_article_standard,
                                    instream_video_desktop, instream_video_mobile, marketplace_mobile,
                                    mobile_feed_basic, mobile_feed_standard, right_column_standard,
                                    suggested_video_desktop, suggested_video_mobile, watch_feed_mobile])

all_instagram_formats = CatalogNode(ContentDeliveryReport.Platform.instagram,
                                    [instagram_standard, instagram_story, instagram_explore_contextual,
                                     instagram_explore_immersive])

all_audience_network_formats = CatalogNode(ContentDeliveryReport.Platform.audience_network,
                                           [audience_network_instream_video, audience_network_instream_video_mobile,
                                            mobile_banner, mobile_fullwidth, mobile_interstitial,
                                            mobile_medium_rectangle, mobile_native])

image = copy.deepcopy(image)
image.children = [all_facebook_formats, all_instagram_formats, all_audience_network_formats]

video = copy.deepcopy(video)
video.children = [all_facebook_formats, all_instagram_formats, all_audience_network_formats]


carousel = copy.deepcopy(carousel)
carousel.children = [all_facebook_formats, all_instagram_formats, all_audience_network_formats]


existing_post_facebook_formats = CatalogNode(ContentDeliveryReport.Platform.facebook, [right_column_standard,
                                                                                       desktop_feed_standard,
                                                                                       mobile_feed_standard])

existing_post_instagram_formats = CatalogNode(ContentDeliveryReport.Platform.instagram,
                                              [instagram_standard])

existing_post = copy.deepcopy(existing_post)
existing_post.children = [existing_post_facebook_formats, existing_post_instagram_formats]


class AdPreviewFormatCatalog(CatalogBase):
    A_image = image
    B_video = video
    C_carousel = carousel
    D_existing_post = existing_post
