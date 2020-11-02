from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport
from facebook_business.adobjects.targeting import Targeting

from FacebookCampaignsBuilder.Api.catalogs import objectives
from FacebookCampaignsBuilder.Api.catalogs.base import Base
from FacebookCampaignsBuilder.Api.catalogs.node import Node

_position = ContentDeliveryReport.Position
_platform = ContentDeliveryReport.Platform
_device_platforms = Targeting.DevicePlatforms

fb_feed = Node(_position.feed)
fb_instant_article = Node(_position.instant_article)
fb_video_feeds = Node(_position.video_feeds)
fb_right_column = Node(_position.right_hand_column)
fb_marketplace = Node(_position.marketplace)
fb_stories = Node(_position.facebook_stories)
fb_search_results = Node(_position.search)
fb_instream_videos = Node(_position.instream_video)

ig_feed = Node(_position.feed)
ig_stories = Node(_position.instagram_stories)
ig_explore = Node(_position.instagram_explore)

an_native = Node(_position.an_classic)
an_in_stream_videos = Node(_position.instream_video)
an_rewarded_videos = Node(_position.rewarded_video)


class Placement(Base):
    brand_awareness = objectives.brand_awareness.with_children(
        Node(
            _device_platforms.mobile,
            Node(_platform.facebook, fb_feed, fb_video_feeds, fb_instant_article, fb_instream_videos, fb_stories),
            Node(_platform.instagram, ig_feed),
            Node(_platform.audience_network, an_native, an_in_stream_videos),
        ),
        Node(
            _device_platforms.desktop,
            Node(_platform.facebook, fb_feed, fb_video_feeds, fb_instream_videos),
            Node(_platform.audience_network, an_native, an_in_stream_videos),
        ),
    )
    reach = objectives.reach.with_children(
        Node(
            _device_platforms.mobile,
            Node(
                _platform.facebook,
                fb_instream_videos,
                fb_stories,
                fb_marketplace,
                fb_video_feeds,
                fb_instant_article,
                fb_feed,
                fb_search_results,
            ),
            Node(_platform.instagram, ig_feed, ig_stories, ig_explore),
            Node(_platform.audience_network, an_in_stream_videos, an_rewarded_videos, an_native),
        ),
        Node(
            _device_platforms.desktop,
            Node(_platform.facebook, fb_instream_videos, fb_marketplace, fb_video_feeds, fb_feed, fb_search_results),
            Node(_platform.audience_network, an_in_stream_videos, an_native, an_rewarded_videos),
        ),
    )
    traffic = objectives.website_traffic.with_children(
        Node(
            _device_platforms.mobile,
            Node(
                _platform.facebook,
                fb_feed,
                fb_instant_article,
                fb_video_feeds,
                fb_right_column,
                fb_marketplace,
                fb_stories,
                fb_instream_videos,
                fb_search_results,
            ),
            Node(_platform.instagram, ig_feed, ig_stories, ig_explore),
            Node(_platform.audience_network, an_native, an_in_stream_videos, an_rewarded_videos),
        ),
        Node(
            _device_platforms.desktop,
            Node(
                _platform.facebook,
                fb_feed,
                fb_marketplace,
                fb_instream_videos,
                fb_right_column,
                fb_search_results,
                fb_video_feeds,
            ),
            Node(_platform.audience_network, an_native, an_in_stream_videos, an_rewarded_videos),
        ),
    )
    video_views = objectives.video_views.with_children(
        Node(
            _device_platforms.mobile,
            Node(
                _platform.facebook,
                fb_feed,
                fb_instant_article,
                fb_marketplace,
                fb_stories,
                fb_instream_videos,
                fb_video_feeds,
                fb_search_results,
            ),
            Node(_platform.instagram, ig_feed, ig_stories, ig_explore),
            Node(_platform.audience_network, an_native, an_rewarded_videos, an_in_stream_videos),
        ),
        Node(
            _device_platforms.desktop,
            Node(_platform.facebook, fb_feed, fb_marketplace, fb_instream_videos, fb_video_feeds, fb_search_results),
            Node(_platform.audience_network, an_in_stream_videos, an_native, an_rewarded_videos),
        ),
    )
    lead_generation = objectives.lead_generation.with_children(
        Node(
            _device_platforms.mobile, Node(_platform.facebook, fb_feed, fb_stories), Node(_platform.instagram, ig_feed),
        ),
        Node(_device_platforms.desktop, Node(_platform.facebook, fb_feed)),
    )
    conversions = objectives.conversions_leaf.with_children(
        Node(
            _device_platforms.mobile,
            Node(
                _platform.facebook,
                fb_feed,
                fb_instant_article,
                fb_video_feeds,
                fb_marketplace,
                fb_stories,
                fb_instream_videos,
                fb_search_results,
                fb_right_column,
            ),
            Node(_platform.instagram, ig_feed, ig_stories, ig_explore),
        ),
        Node(
            _device_platforms.desktop,
            Node(
                _platform.facebook,
                fb_feed,
                fb_video_feeds,
                fb_right_column,
                fb_search_results,
                fb_instream_videos,
                fb_marketplace,
            ),
            Node(_platform.audience_network, an_native, an_in_stream_videos, an_rewarded_videos),
        ),
    )
    catalog_sales = objectives.catalog_sales.with_children(
        Node(
            _device_platforms.mobile,
            Node(
                _platform.facebook,
                fb_feed,
                fb_video_feeds,
                fb_search_results,
                fb_instream_videos,
                fb_marketplace,
                fb_right_column,
                fb_instant_article,
                fb_stories,
            ),
            Node(_platform.instagram, ig_feed, ig_stories, ig_explore),
            Node(_platform.audience_network, an_native, an_in_stream_videos, an_rewarded_videos),
        ),
        Node(
            _device_platforms.desktop,
            Node(
                _platform.facebook,
                fb_instream_videos,
                fb_marketplace,
                fb_right_column,
                fb_feed,
                fb_video_feeds,
                fb_search_results,
            ),
            Node(_platform.audience_network, an_in_stream_videos, an_rewarded_videos, an_native),
        ),
    )
    post_likes = objectives.post_likes.with_children(
        Node(
            _device_platforms.mobile,
            Node(
                _platform.facebook,
                fb_instream_videos,
                fb_marketplace,
                fb_stories,
                fb_search_results,
                fb_feed,
                fb_instant_article,
                fb_video_feeds,
            ),
            Node(_platform.instagram, ig_feed, ig_stories, ig_explore),
        ),
        Node(
            _device_platforms.desktop,
            Node(_platform.facebook, fb_instream_videos, fb_feed, fb_video_feeds, fb_marketplace, fb_search_results),
        ),
    )
    page_likes = objectives.page_likes.with_children(
        Node(
            _device_platforms.mobile,
            Node(
                _platform.facebook,
                fb_instream_videos,
                fb_marketplace,
                fb_search_results,
                fb_video_feeds,
                fb_feed,
                fb_stories,
                fb_instant_article,
            ),
        ),
        Node(
            _device_platforms.desktop,
            Node(_platform.facebook, fb_instream_videos, fb_feed, fb_search_results, fb_marketplace, fb_video_feeds),
        ),
    )
    app_installs = objectives.app_installs.with_children(
        Node(
            _device_platforms.mobile,
            Node(_platform.facebook, fb_feed, fb_video_feeds, fb_instant_article, fb_stories),
            Node(_platform.instagram, ig_feed, ig_stories, ig_explore),
            Node(_platform.audience_network, an_native, an_rewarded_videos),
        ),
        Node(_device_platforms.desktop, Node(_platform.facebook, fb_feed, fb_video_feeds)),
    )
    store_traffic = objectives.store_traffic.with_children(
        Node(
            _device_platforms.mobile,
            Node(
                _platform.facebook,
                fb_instream_videos,
                fb_marketplace,
                fb_stories,
                fb_instant_article,
                fb_feed,
                fb_video_feeds,
                fb_search_results,
            ),
        ),
        Node(
            _device_platforms.desktop,
            Node(_platform.facebook, fb_feed, fb_search_results, fb_marketplace, fb_video_feeds, fb_instream_videos),
        ),
    )
