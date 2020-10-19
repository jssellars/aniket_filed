from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport
from facebook_business.adobjects.targeting import Targeting

from PotterFacebookCampaignsBuilder.Api.catalogs import objectives
from PotterFacebookCampaignsBuilder.Api.catalogs.base import Base
from PotterFacebookCampaignsBuilder.Api.catalogs.node import Node

_position = ContentDeliveryReport.Position
_platform = ContentDeliveryReport.Platform
_device_platforms = Targeting.DevicePlatforms

facebook_feed = Node(_position.feed)
facebook_instant_article = Node(_position.instant_article)
facebook_video_feeds = Node(_position.video_feeds)
facebook_right_column = Node(_position.right_hand_column)
facebook_marketplace = Node(_position.marketplace)
facebook_stories = Node(_position.facebook_stories)
facebook_search_results = Node(_position.search)
facebook_in_stream_videos = Node(_position.instream_video)

instagram_feed = Node(_position.feed)
instagram_stories = Node(_position.instagram_stories)
instagram_explore = Node(_position.instagram_explore)

audience_network_native = Node(_position.an_classic)
audience_network_in_stream_videos = Node(_position.instream_video)
audience_network_rewarded_videos = Node(_position.rewarded_video)

app_installs_mobile_facebook = Node(
    _platform.facebook, facebook_feed, facebook_video_feeds, facebook_instant_article, facebook_stories,
)
app_installs_mobile_instagram = Node(_platform.instagram, instagram_feed, instagram_stories, instagram_explore)
app_installs_mobile_audience_network = Node(
    _platform.audience_network, audience_network_native, audience_network_rewarded_videos,
)

app_installs_mobile = Node(
    _device_platforms.mobile,
    app_installs_mobile_facebook,
    app_installs_mobile_instagram,
    app_installs_mobile_audience_network,
)
app_installs_desktop_facebook = Node(_platform.facebook, facebook_feed, facebook_video_feeds)
app_installs_desktop = Node(_device_platforms.desktop, app_installs_desktop_facebook)


brand_awareness_mobile_facebook = Node(
    _platform.facebook,
    facebook_feed,
    facebook_video_feeds,
    facebook_instant_article,
    facebook_in_stream_videos,
    facebook_stories,
)
brand_awareness_mobile_instagram = Node(_platform.instagram, instagram_feed)
brand_awareness_mobile_audience_network = Node(
    _platform.audience_network, audience_network_native, audience_network_in_stream_videos,
)
brand_awareness_mobile = Node(
    _device_platforms.mobile,
    brand_awareness_mobile_facebook,
    brand_awareness_mobile_instagram,
    brand_awareness_mobile_audience_network,
)
brand_awareness_desktop_facebook = Node(
    _platform.facebook, facebook_feed, facebook_video_feeds, facebook_in_stream_videos,
)
brand_awareness_desktop_audience_network = Node(
    _platform.audience_network, audience_network_native, audience_network_in_stream_videos,
)
brand_awareness_desktop = Node(
    _device_platforms.desktop, brand_awareness_desktop_facebook, brand_awareness_desktop_audience_network
)


catalog_sales_mobile_facebook = Node(
    _platform.facebook,
    facebook_feed,
    facebook_video_feeds,
    facebook_search_results,
    facebook_in_stream_videos,
    facebook_marketplace,
    facebook_right_column,
    facebook_instant_article,
    facebook_stories,
)
catalog_sales_mobile_instagram = Node(_platform.instagram, instagram_feed, instagram_stories, instagram_explore)
catalog_sales_mobile_audience_network = Node(
    _platform.audience_network,
    audience_network_native,
    audience_network_in_stream_videos,
    audience_network_rewarded_videos,
)
catalog_sales_mobile = Node(
    _device_platforms.mobile,
    catalog_sales_mobile_facebook,
    catalog_sales_mobile_instagram,
    catalog_sales_mobile_audience_network,
)
catalog_sales_desktop_facebook = Node(
    _platform.facebook,
    facebook_in_stream_videos,
    facebook_marketplace,
    facebook_right_column,
    facebook_feed,
    facebook_video_feeds,
    facebook_search_results,
)
catalog_sales_desktop_audience_network = Node(
    _platform.audience_network,
    audience_network_in_stream_videos,
    audience_network_rewarded_videos,
    audience_network_native,
)
catalog_sales_desktop = Node(
    _device_platforms.desktop, catalog_sales_desktop_facebook, catalog_sales_desktop_audience_network
)


conversions_mobile_facebook = Node(
    _platform.facebook,
    facebook_feed,
    facebook_instant_article,
    facebook_video_feeds,
    facebook_marketplace,
    facebook_stories,
    facebook_in_stream_videos,
    facebook_search_results,
    facebook_right_column,
)
conversions_mobile_instagram = Node(_platform.instagram, instagram_feed, instagram_stories, instagram_explore)
conversions_mobile = Node(_device_platforms.mobile, conversions_mobile_facebook, conversions_mobile_instagram)
conversions_desktop_facebook = Node(
    _platform.facebook,
    facebook_feed,
    facebook_video_feeds,
    facebook_right_column,
    facebook_search_results,
    facebook_in_stream_videos,
    facebook_marketplace,
)
conversions_desktop_audience_network = Node(
    _platform.audience_network,
    audience_network_native,
    audience_network_in_stream_videos,
    audience_network_rewarded_videos,
)
conversions_desktop = Node(
    _device_platforms.desktop, conversions_desktop_facebook, conversions_desktop_audience_network
)


lead_generation_mobile_facebook = Node(_platform.facebook, facebook_feed, facebook_stories)
lead_generation_mobile_instagram = Node(_platform.instagram, instagram_feed)
lead_generation_mobile = Node(
    _device_platforms.mobile, lead_generation_mobile_facebook, lead_generation_mobile_instagram
)
lead_generation_desktop_facebook = Node(_platform.facebook, facebook_feed)
lead_generation_desktop = Node(_device_platforms.desktop, lead_generation_desktop_facebook)


page_likes_mobile_facebook = Node(
    _platform.facebook,
    facebook_in_stream_videos,
    facebook_marketplace,
    facebook_search_results,
    facebook_video_feeds,
    facebook_feed,
    facebook_stories,
    facebook_instant_article,
)
page_likes_mobile = Node(_device_platforms.mobile, page_likes_mobile_facebook)
page_likes_desktop_facebook = Node(
    _platform.facebook,
    facebook_in_stream_videos,
    facebook_feed,
    facebook_search_results,
    facebook_marketplace,
    facebook_video_feeds,
)
page_likes_desktop = Node(_device_platforms.desktop, page_likes_desktop_facebook)


post_likes_mobile_facebook = Node(
    _platform.facebook,
    facebook_in_stream_videos,
    facebook_marketplace,
    facebook_stories,
    facebook_search_results,
    facebook_feed,
    facebook_instant_article,
    facebook_video_feeds,
)
post_likes_mobile_instagram = Node(_platform.instagram, instagram_feed, instagram_stories, instagram_explore)
post_likes_mobile = Node(_device_platforms.mobile, post_likes_mobile_facebook, post_likes_mobile_instagram)
post_likes_desktop_facebook = Node(
    _platform.facebook,
    facebook_in_stream_videos,
    facebook_feed,
    facebook_video_feeds,
    facebook_marketplace,
    facebook_search_results,
)
post_likes_desktop = Node(_device_platforms.desktop, post_likes_desktop_facebook)


reach_mobile_facebook = Node(
    _platform.facebook,
    facebook_in_stream_videos,
    facebook_stories,
    facebook_marketplace,
    facebook_video_feeds,
    facebook_instant_article,
    facebook_feed,
    facebook_search_results,
)
reach_mobile_instagram = Node(_platform.instagram, instagram_feed, instagram_stories, instagram_explore)
reach_mobile_audience_network = Node(
    _platform.audience_network,
    audience_network_in_stream_videos,
    audience_network_rewarded_videos,
    audience_network_native,
)
reach_mobile = Node(
    _device_platforms.mobile, reach_mobile_facebook, reach_mobile_instagram, reach_mobile_audience_network
)
reach_desktop_facebook = Node(
    _platform.facebook,
    facebook_in_stream_videos,
    facebook_marketplace,
    facebook_video_feeds,
    facebook_feed,
    facebook_search_results,
)
reach_desktop_audience_network = Node(
    _platform.audience_network,
    audience_network_in_stream_videos,
    audience_network_native,
    audience_network_rewarded_videos,
)
reach_desktop = Node(_device_platforms.desktop, reach_desktop_facebook, reach_desktop_audience_network)


store_traffic_mobile_facebook = Node(
    _platform.facebook,
    facebook_in_stream_videos,
    facebook_marketplace,
    facebook_stories,
    facebook_instant_article,
    facebook_feed,
    facebook_video_feeds,
    facebook_search_results,
)
store_traffic_mobile = Node(_device_platforms.mobile, store_traffic_mobile_facebook)
store_traffic_desktop_facebook = Node(
    _platform.facebook,
    facebook_feed,
    facebook_search_results,
    facebook_marketplace,
    facebook_video_feeds,
    facebook_in_stream_videos,
)
store_traffic_desktop = Node(_device_platforms.desktop, store_traffic_desktop_facebook)


traffic_mobile_facebook = Node(
    _platform.facebook,
    facebook_feed,
    facebook_instant_article,
    facebook_video_feeds,
    facebook_right_column,
    facebook_marketplace,
    facebook_stories,
    facebook_in_stream_videos,
    facebook_search_results,
)
traffic_mobile_instagram = Node(_platform.instagram, instagram_feed, instagram_stories, instagram_explore)
traffic_mobile_audience_network = Node(
    _platform.audience_network,
    audience_network_native,
    audience_network_in_stream_videos,
    audience_network_rewarded_videos,
)
traffic_mobile = Node(
    _device_platforms.mobile, traffic_mobile_facebook, traffic_mobile_instagram, traffic_mobile_audience_network,
)
traffic_desktop_facebook = Node(
    _platform.facebook,
    facebook_feed,
    facebook_marketplace,
    facebook_in_stream_videos,
    facebook_right_column,
    facebook_search_results,
    facebook_video_feeds,
)
traffic_desktop_audience_network = Node(
    _platform.audience_network,
    audience_network_native,
    audience_network_in_stream_videos,
    audience_network_rewarded_videos,
)
traffic_desktop = Node(_device_platforms.desktop, traffic_desktop_facebook, traffic_desktop_audience_network)


video_views_mobile_facebook = Node(
    _platform.facebook,
    facebook_feed,
    facebook_instant_article,
    facebook_marketplace,
    facebook_stories,
    facebook_in_stream_videos,
    facebook_video_feeds,
    facebook_search_results,
)
video_views_mobile_instagram = Node(_platform.instagram, instagram_feed, instagram_stories, instagram_explore)
video_views_mobile_audience_network = Node(
    _platform.audience_network,
    audience_network_native,
    audience_network_rewarded_videos,
    audience_network_in_stream_videos,
)
video_views_mobile = Node(
    _device_platforms.mobile,
    video_views_mobile_facebook,
    video_views_mobile_instagram,
    video_views_mobile_audience_network,
)
video_views_desktop_facebook = Node(
    _platform.facebook,
    facebook_feed,
    facebook_marketplace,
    facebook_in_stream_videos,
    facebook_video_feeds,
    facebook_search_results,
)
video_views_desktop_audience_network = Node(
    _platform.audience_network,
    audience_network_in_stream_videos,
    audience_network_native,
    audience_network_rewarded_videos,
)
video_views_desktop = Node(
    _device_platforms.desktop, video_views_desktop_facebook, video_views_desktop_audience_network
)


class Placement(Base):
    A_brand_awareness = objectives.brand_awareness.with_children(brand_awareness_mobile, brand_awareness_desktop)
    B_reach = objectives.reach.with_children(reach_mobile, reach_desktop)
    C_traffic = objectives.website_traffic.with_children(traffic_mobile, traffic_desktop)
    D_video_views = objectives.video_views.with_children(video_views_mobile, video_views_desktop)
    E_lead_generation = objectives.lead_generation.with_children(lead_generation_mobile, lead_generation_desktop)
    F_conversions = objectives.conversions_leaf.with_children(conversions_mobile, conversions_desktop)
    G_catalog_sales = objectives.catalog_sales.with_children(catalog_sales_mobile, catalog_sales_desktop)
    F_post_likes = objectives.post_likes.with_children(post_likes_mobile, post_likes_desktop)
    H_page_likes = objectives.page_likes.with_children(page_likes_mobile, page_likes_desktop)
    I_app_installs = objectives.app_installs.with_children(app_installs_mobile, app_installs_desktop)
    J_store_traffic = objectives.store_traffic.with_children(store_traffic_mobile, store_traffic_desktop)
