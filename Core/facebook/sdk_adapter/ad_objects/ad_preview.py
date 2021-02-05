from enum import Enum

from facebook_business.adobjects.adpreview import AdPreview

from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum

# TODO: documentation link(s)

_format = AdPreview.AdFormat


@cat_enum
class AdFormat(Enum):
    AUDIENCE_NETWORK_INSTREAM_VIDEO = Cat(
        _format.audience_network_instream_video, display_name="Apps & Sites Instream Video"
    )
    AUDIENCE_NETWORK_INSTREAM_VIDEO_MOBILE = Cat(
        _format.audience_network_instream_video_mobile, display_name="Apps & Sites Mobile Video"
    )
    AUDIENCE_NETWORK_OUTSTREAM_VIDEO = Cat(_format.audience_network_outstream_video)
    AUDIENCE_NETWORK_REWARDED_VIDEO = Cat(_format.audience_network_rewarded_video)
    DESKTOP_FEED_STANDARD = Cat(_format.desktop_feed_standard, display_name="Facebook Desktop Feed")
    FACEBOOK_STORY_MOBILE = Cat(_format.facebook_story_mobile, display_name="Facebook Story")
    INSTAGRAM_EXPLORE_CONTEXTUAL = Cat(_format.instagram_explore_contextual)
    INSTAGRAM_EXPLORE_IMMERSIVE = Cat(_format.instagram_explore_immersive)
    INSTAGRAM_STANDARD = Cat(_format.instagram_standard)
    INSTAGRAM_STORY = Cat(_format.instagram_story)
    INSTANT_ARTICLE_RECIRCULATION_AD = Cat(_format.instant_article_recirculation_ad)
    INSTANT_ARTICLE_STANDARD = Cat(_format.instant_article_standard)
    INSTREAM_VIDEO_DESKTOP = Cat(_format.instream_video_desktop)
    INSTREAM_VIDEO_MOBILE = Cat(_format.instream_video_mobile)
    JOB_BROWSER_DESKTOP = Cat(_format.job_browser_desktop)  # unused in group
    JOB_BROWSER_MOBILE = Cat(_format.job_browser_mobile)  # unused in group
    MARKETPLACE_MOBILE = Cat(_format.marketplace_mobile)
    MESSENGER_MOBILE_INBOX_MEDIA = Cat(_format.messenger_mobile_inbox_media)
    MESSENGER_MOBILE_STORY_MEDIA = Cat(_format.messenger_mobile_story_media)
    MOBILE_BANNER = Cat(_format.mobile_banner)
    MOBILE_FEED_BASIC = Cat(_format.mobile_feed_basic)
    MOBILE_FEED_STANDARD = Cat(_format.mobile_feed_standard, display_name="Facebook Mobile News Feed")
    MOBILE_FULLWIDTH = Cat(_format.mobile_fullwidth)  # uncertain inclusion in group
    MOBILE_INTERSTITIAL = Cat(_format.mobile_interstitial)
    MOBILE_MEDIUM_RECTANGLE = Cat(_format.mobile_medium_rectangle)
    MOBILE_NATIVE = Cat(_format.mobile_native)
    RIGHT_COLUMN_STANDARD = Cat(_format.right_column_standard)
    SUGGESTED_VIDEO_DESKTOP = Cat(_format.suggested_video_desktop)
    SUGGESTED_VIDEO_MOBILE = Cat(_format.suggested_video_mobile)
    WATCH_FEED_MOBILE = Cat(_format.watch_feed_mobile)
