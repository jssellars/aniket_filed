from facebook_business.adobjects.adpreview import AdPreview
from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport

from FacebookCampaignsBuilder.Api.catalogs import ad_format
from FacebookCampaignsBuilder.Api.catalogs.base import Base
from FacebookCampaignsBuilder.Api.catalogs.node import Node

_format = AdPreview.AdFormat
_platform = ContentDeliveryReport.Platform

all_facebook_formats = Node(
    _platform.facebook,
    _format.desktop_feed_standard,
    _format.facebook_story_mobile,
    _format.instant_article_standard,
    _format.instream_video_desktop,
    _format.instream_video_mobile,
    _format.marketplace_mobile,
    _format.mobile_feed_basic,
    _format.mobile_feed_standard,
    _format.right_column_standard,
    _format.suggested_video_desktop,
    _format.suggested_video_mobile,
    _format.watch_feed_mobile,
)
all_instagram_formats = Node(
    _platform.instagram,
    _format.instagram_standard,
    _format.instagram_story,
    _format.instagram_explore_contextual,
    _format.instagram_explore_immersive,
)
all_audience_network_formats = Node(
    _platform.audience_network,
    _format.audience_network_instream_video,
    _format.audience_network_instream_video_mobile,
    _format.mobile_banner,
    _format.mobile_fullwidth,
    _format.mobile_interstitial,
    _format.mobile_medium_rectangle,
    _format.mobile_native,
)
existing_post_facebook_formats = Node(
    _platform.facebook, _format.right_column_standard, _format.desktop_feed_standard, _format.mobile_feed_standard
)
existing_post_instagram_formats = Node(_platform.instagram, _format.instagram_standard)


class AdPreviewFormat(Base):
    A_image = ad_format.image.with_children(all_facebook_formats, all_instagram_formats, all_audience_network_formats)
    B_video = ad_format.video.with_children(all_facebook_formats, all_instagram_formats, all_audience_network_formats)
    C_carousel = ad_format.carousel.with_children(
        all_facebook_formats, all_instagram_formats, all_audience_network_formats
    )
    D_existing_post = ad_format.existing_post.with_children(
        existing_post_facebook_formats, existing_post_instagram_formats
    )
