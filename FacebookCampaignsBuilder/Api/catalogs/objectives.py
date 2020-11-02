from facebook_business.adobjects.adpreview import AdPreview
from facebook_business.adobjects.campaign import Campaign

from FacebookCampaignsBuilder.Api.catalogs.base import Base
from FacebookCampaignsBuilder.Api.catalogs.node import Node
from FacebookCampaignsBuilder.Api.catalogs import optimization_goal

from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers import GraphAPIAdPreviewBuilderHandler


_media_format = GraphAPIAdPreviewBuilderHandler.FiledAdFormatEnum
media_formats = "MEDIA_FORMATS"

_mf_img = _media_format.IMAGE.name
_mf_vid = _media_format.VIDEO.name
_mf_car = _media_format.CAROUSEL.name
_mf_col = _media_format.COLLECTION.name

# https://www.facebook.com/business/help/279271845888065

_format = AdPreview.AdFormat


class AdFormat:
    audience_network_instream_video = Node(_format.audience_network_instream_video)
    audience_network_instream_video_mobile = Node(_format.audience_network_instream_video_mobile)
    audience_network_outstream_video = Node(_format.audience_network_outstream_video)
    audience_network_rewarded_video = Node(_format.audience_network_rewarded_video)
    desktop_feed_standard = Node(_format.desktop_feed_standard)
    facebook_story_mobile = Node(_format.facebook_story_mobile)
    instagram_explore_contextual = Node(_format.instagram_explore_contextual)
    instagram_explore_immersive = Node(_format.instagram_explore_immersive)
    instagram_standard = Node(_format.instagram_standard)
    instagram_story = Node(_format.instagram_story)
    instant_article_recirculation_ad = Node(_format.instant_article_recirculation_ad)
    instant_article_standard = Node(_format.instant_article_standard)
    instream_video_desktop = Node(_format.instream_video_desktop)
    instream_video_mobile = Node(_format.instream_video_mobile)
    job_browser_desktop = Node(_format.job_browser_desktop)  #  unused
    job_browser_mobile = Node(_format.job_browser_mobile)  #  unused
    marketplace_mobile = Node(_format.marketplace_mobile)
    messenger_mobile_inbox_media = Node(_format.messenger_mobile_inbox_media)
    messenger_mobile_story_media = Node(_format.messenger_mobile_story_media)
    mobile_banner = Node(_format.mobile_banner)
    mobile_feed_basic = Node(_format.mobile_feed_basic)
    mobile_feed_standard = Node(_format.mobile_feed_standard)
    mobile_fullwidth = Node(_format.mobile_fullwidth)  # uncertain
    mobile_interstitial = Node(_format.mobile_interstitial)
    mobile_medium_rectangle = Node(_format.mobile_medium_rectangle)
    mobile_native = Node(_format.mobile_native)
    right_column_standard = Node(_format.right_column_standard)
    suggested_video_desktop = Node(_format.suggested_video_desktop)
    suggested_video_mobile = Node(_format.suggested_video_mobile)
    watch_feed_mobile = Node(_format.watch_feed_mobile)


ad_format_groups = "AD_FORMAT_GROUPS"


class AdFormatGroup(Base):
    facebook_feed = Node(
        "FACEBOOK_FEED",
        AdFormat.desktop_feed_standard,
        AdFormat.mobile_feed_basic,
        AdFormat.mobile_feed_standard,
        AdFormat.watch_feed_mobile,
    )  # ??? mobile should also be in instagram ???
    facebook_right_column = Node("FACEBOOK_RIGHT_COLUMN", AdFormat.right_column_standard)
    facebook_instant_articles = Node(
        "FACEBOOK_INSTANT_ARTICLES", AdFormat.instant_article_standard, AdFormat.instant_article_recirculation_ad
    )
    facebook_in_stream_video = Node(
        "FACEBOOK_IN_STREAM_VIDEO", AdFormat.instream_video_desktop, AdFormat.instream_video_mobile
    )
    facebook_marketplace = Node("FACEBOOK_MARKETPLACE", AdFormat.marketplace_mobile)
    facebook_stories = Node("FACEBOOK_STORIES", AdFormat.facebook_story_mobile)
    facebook_search_results = Node(
        "FACEBOOK_SEARCH_RESULTS", AdFormat.mobile_medium_rectangle, AdFormat.mobile_fullwidth
    )  # ??? mobile_fullwidth not certain ???
    facebook_video_feeds = Node(
        "FACEBOOK_VIDEO_FEEDS", AdFormat.suggested_video_desktop, AdFormat.suggested_video_mobile
    )
    instagram_stories = Node("INSTAGRAM_STORIES", AdFormat.instagram_story)
    instagram_feed = Node("INSTAGRAM_FEED", AdFormat.instagram_standard)
    instagram_explore = Node(
        "INSTAGRAM_EXPLORE", AdFormat.instagram_explore_contextual, AdFormat.instagram_explore_immersive
    )
    audience_network_native_banner_interstitial = Node(
        "AUDIENCE_NETWORK_NATIVE_BANNER_INTERSTITIAL",
        AdFormat.mobile_native,
        AdFormat.mobile_banner,
        AdFormat.mobile_interstitial,
    )
    audience_network_rewarded_video = Node(
        "AUDIENCE_NETWORK_REWARDED_VIDEO",
        AdFormat.audience_network_rewarded_video,
        AdFormat.audience_network_instream_video,
        AdFormat.audience_network_instream_video_mobile,
        AdFormat.audience_network_outstream_video,
    )
    # sponsored_message = Node("SPONSORED_MESSAGE")  # unclear which AdFormat to map to # disabled for now
    messenger_inbox = Node("MESSENGER_INBOX", AdFormat.messenger_mobile_inbox_media)
    messenger_stories = Node("MESSENGER_STORIES", AdFormat.messenger_mobile_story_media)


# https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group#parameters-2
# https://www.facebook.com/business/help/1438417719786914
# https://developers.facebook.com/docs/marketing-api/bidding/overview#opt

_objective = Campaign.Objective
_goal = optimization_goal.OptimizationGoalWithBillingEvents
goals = "OPTIMIZATON_GOALS_FOR_ALL"
goals_instant_experiences_app = "OPTIMIZATON_GOALS_FOR_INSTANT_EXPERIENCES_APP"
goals_mobile_app = "OPTIMIZATON_GOALS_FOR_MOBILE_APP"
goals_event = "OPTIMIZATON_GOALS_FOR_EVENT"
goals_page_post = "OPTIMIZATON_GOALS_FOR_PAGE_POST"

# Conversions
store_traffic = Node(
    _objective.local_awareness,
    Node(
        ad_format_groups,
        AdFormatGroup.facebook_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car, _mf_col)),
        AdFormatGroup.facebook_marketplace.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car, _mf_col)),
    ),
)
conversions_leaf = Node(
    _objective.conversions,
    Node(
        goals,
        _goal.offsite_conversions,
        _goal.impressions,
        _goal.post_engagement,
        _goal.reach,
        _goal.social_impressions,
        _goal.value,
        _goal.landing_page_views,
        _goal.link_clicks,
    ),
    Node(
        ad_format_groups,
        AdFormatGroup.facebook_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car, _mf_col)),
        AdFormatGroup.facebook_right_column.with_children(Node(media_formats, _mf_img, _mf_car)),
        AdFormatGroup.facebook_instant_articles.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_in_stream_video.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.facebook_marketplace.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_search_results.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_video_feeds.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.instagram_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car, _mf_col)),
        AdFormatGroup.instagram_explore.with_children(Node(media_formats, _mf_img, _mf_vid)),
        AdFormatGroup.audience_network_native_banner_interstitial.with_children(
            Node(media_formats, _mf_img, _mf_vid, _mf_car)
        ),
        AdFormatGroup.audience_network_rewarded_video.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.messenger_inbox.with_children(Node(media_formats, _mf_img, _mf_car)),
        AdFormatGroup.messenger_stories.with_children(Node(media_formats, _mf_img, _mf_vid)),
    ),
)
catalog_sales = Node(
    _objective.product_catalog_sales,
    Node(
        goals,
        _goal.offsite_conversions,
        _goal.impressions,
        _goal.post_engagement,
        _goal.offsite_conversions,
        _goal.reach,
        _goal.link_clicks,
    ),
    Node(
        ad_format_groups,
        AdFormatGroup.facebook_feed.with_children(Node(media_formats, _mf_img, _mf_car, _mf_col)),
        AdFormatGroup.facebook_right_column.with_children(Node(media_formats, _mf_img, _mf_car)),
        AdFormatGroup.facebook_marketplace.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_stories.with_children(Node(media_formats, _mf_car)),
        AdFormatGroup.facebook_search_results.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_explore.with_children(Node(media_formats, _mf_img)),
        AdFormatGroup.audience_network_native_banner_interstitial.with_children(Node(media_formats, _mf_img, _mf_car)),
        AdFormatGroup.messenger_inbox.with_children(Node(media_formats, _mf_img, _mf_car)),
    ),
)

# Awareness
brand_awareness = Node(
    _objective.brand_awareness,
    Node(goals, _goal.ad_recall_lift),
    Node(
        ad_format_groups,
        AdFormatGroup.facebook_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_instant_articles.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_in_stream_video.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.facebook_marketplace.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_search_results.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_video_feeds.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.instagram_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_explore.with_children(Node(media_formats, _mf_img, _mf_vid)),
        AdFormatGroup.messenger_stories.with_children(Node(media_formats, _mf_img, _mf_vid)),
    ),
)

reach = Node(
    _objective.reach,
    Node(goals, _goal.reach, _goal.impressions),
    Node(
        ad_format_groups,
        AdFormatGroup.facebook_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_instant_articles.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_in_stream_video.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.facebook_marketplace.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_search_results.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_video_feeds.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.instagram_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_explore.with_children(Node(media_formats, _mf_img, _mf_vid)),
        AdFormatGroup.audience_network_native_banner_interstitial.with_children(
            Node(media_formats, _mf_img, _mf_vid, _mf_car)
        ),
        AdFormatGroup.messenger_stories.with_children(Node(media_formats, _mf_img, _mf_vid)),
    ),
)

# App Activity
app_traffic = Node(
    _objective.link_clicks,
    Node(goals, _goal.link_clicks, _goal.impressions, _goal.post_engagement, _goal.reach, _goal.landing_page_views),
    Node(
        goals_instant_experiences_app,
        _goal.engaged_users,
        _goal.app_installs,
        _goal.impressions,
        _goal.post_engagement,
        _goal.reach,
    ),
    Node(goals_mobile_app, _goal.link_clicks, _goal.impressions, _goal.reach, _goal.offsite_conversions),
    Node(
        ad_format_groups,
        AdFormatGroup.facebook_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car, _mf_col)),
        AdFormatGroup.facebook_right_column.with_children(Node(media_formats, _mf_img, _mf_car)),
        AdFormatGroup.facebook_instant_articles.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_in_stream_video.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.facebook_marketplace.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_search_results.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_video_feeds.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.instagram_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car, _mf_col)),
        AdFormatGroup.audience_network_native_banner_interstitial.with_children(
            Node(media_formats, _mf_img, _mf_vid, _mf_car)
        ),
        AdFormatGroup.messenger_inbox.with_children(Node(media_formats, _mf_img, _mf_car)),
        AdFormatGroup.messenger_stories.with_children(Node(media_formats, _mf_img, _mf_vid)),
    ),
)
app_installs = Node(
    _objective.app_installs,
    Node(goals_instant_experiences_app, _goal.app_installs, _goal.impressions, _goal.post_engagement),
    Node(goals_mobile_app, _goal.app_installs, _goal.offsite_conversions, _goal.link_clicks, _goal.reach, _goal.value),
    Node(
        ad_format_groups,
        AdFormatGroup.facebook_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_instant_articles.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_in_stream_video.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.facebook_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_search_results.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_video_feeds.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.instagram_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_explore.with_children(Node(media_formats, _mf_img, _mf_vid)),
        AdFormatGroup.audience_network_native_banner_interstitial.with_children(
            Node(media_formats, _mf_img, _mf_vid, _mf_car)
        ),
        AdFormatGroup.audience_network_rewarded_video.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.messenger_inbox.with_children(Node(media_formats, _mf_img, _mf_car)),
        AdFormatGroup.messenger_stories.with_children(Node(media_formats, _mf_img, _mf_vid)),
    ),
)

# Engagement
post_likes = Node(
    _objective.post_engagement, Node(goals, _goal.post_engagement, _goal.impressions, _goal.reach, _goal.link_clicks)
)
page_likes = Node(
    _objective.page_likes,
    Node(goals, _goal.page_likes, _goal.impressions, _goal.post_engagement, _goal.reach),
    Node(ad_format_groups, AdFormatGroup.facebook_feed.with_children(Node(media_formats, _mf_img, _mf_vid))),
)

# Event responses - not selectable yet
event_responses = Node(
    _objective.event_responses,
    Node(goals_event, _goal.event_responses, _goal.impressions, _goal.reach),
    Node(goals_page_post, _goal.event_responses, _goal.impressions, _goal.post_engagement, _goal.reach),
    Node(
        ad_format_groups,
        AdFormatGroup.facebook_feed.with_children(Node(media_formats, _mf_img, _mf_vid)),
        AdFormatGroup.facebook_marketplace.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
    ),
)

# Consideration
engagement = Node(
    "ENGAGEMENT",
    post_likes,
    page_likes,
    Node(
        ad_format_groups,
        AdFormatGroup.facebook_feed.with_children(Node(media_formats, _mf_img, _mf_vid)),
        AdFormatGroup.facebook_instant_articles.with_children(Node(media_formats, _mf_img, _mf_vid)),
        AdFormatGroup.facebook_in_stream_video.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.facebook_search_results.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_video_feeds.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.instagram_feed.with_children(Node(media_formats, _mf_img, _mf_vid)),
        AdFormatGroup.instagram_explore.with_children(Node(media_formats, _mf_img, _mf_vid)),
    ),
)
video_views = Node(
    _objective.video_views,
    Node(goals, _goal.thruplay, _goal.two_second_continuous_video_views),
    Node(
        ad_format_groups,
        AdFormatGroup.facebook_feed.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.facebook_instant_articles.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.facebook_in_stream_video.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.facebook_marketplace.with_children(Node(media_formats, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_search_results.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_video_feeds.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.instagram_stories.with_children(Node(media_formats, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_feed.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.instagram_explore.with_children(Node(media_formats, _mf_img, _mf_vid)),
        AdFormatGroup.audience_network_native_banner_interstitial.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.messenger_stories.with_children(Node(media_formats, _mf_vid)),
    ),
)
lead_generation = Node(
    _objective.lead_generation,
    Node(goals, _goal.lead_generation),
    Node(
        ad_format_groups,
        AdFormatGroup.facebook_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_instant_articles.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_in_stream_video.with_children(Node(media_formats, _mf_vid)),
        AdFormatGroup.facebook_marketplace.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_search_results.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_explore.with_children(Node(media_formats, _mf_img, _mf_vid)),
    ),
)
# Default: REPLIES / Other valid: REPLIES (Click-to-Messenger), IMPRESSIONS (Sponsored Messages)
# TODO: see how to include Click-to-Messenger and Sponsored Messages in the structure
messages = Node(
    _objective.messages,
    Node(goals, _goal.replies, _goal.impressions),
    Node(
        ad_format_groups,
        AdFormatGroup.facebook_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_marketplace.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.facebook_stories.with_children(Node(media_formats, _mf_car)),
        AdFormatGroup.facebook_search_results.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_stories.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_feed.with_children(Node(media_formats, _mf_img, _mf_vid, _mf_car)),
        AdFormatGroup.instagram_explore.with_children(Node(media_formats, _mf_img, _mf_vid)),
        # disabled for now
        # AdFormatGroup.sponsored_message.with_children(Node(media_formats, _mf_img)),
        AdFormatGroup.messenger_inbox.with_children(Node(media_formats, _mf_img, _mf_car)),
    ),
)
website_traffic = app_traffic


class Objectives(Base):
    awareness = Node("AWARENESS", brand_awareness, reach)
    # The messages objective is also conceptually here, but we do not support it (yet)
    consideration = Node("CONSIDERATION", website_traffic, engagement, video_views, lead_generation)
    # The store traffic objective is also conceptually here, but we do not support it (yet)
    conversions = Node(_objective.conversions, catalog_sales, conversions_leaf, store_traffic)
    app_activity = Node("App Activity", app_traffic, app_installs, conversions_leaf)
