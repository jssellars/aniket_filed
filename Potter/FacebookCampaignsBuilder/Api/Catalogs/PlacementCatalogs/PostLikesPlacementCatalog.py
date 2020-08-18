import copy
from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport
from facebook_business.adobjects.targeting import Targeting
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.Placements import facebook_stories_placement, \
    facebook_instant_article_placement, facebook_feed_placement, facebook_marketplace_placement, \
    facebook_in_stream_videos_placement, facebook_search_results_placement, facebook_video_feeds_placement, \
    instagram_feed_placement, instagram_stories_placement, instagram_explore_placement

from Potter.FacebookCampaignsBuilder.Api.Catalogs.ObjectivesCatalog import post_likes

post_likes_mobile_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook,
                                         [facebook_in_stream_videos_placement, facebook_marketplace_placement, facebook_stories_placement,
                                          facebook_search_results_placement, facebook_feed_placement, facebook_instant_article_placement,
                                          facebook_video_feeds_placement])
post_likes_mobile_instagram = CatalogNode(ContentDeliveryReport.Platform.instagram,
                                          [instagram_feed_placement, instagram_stories_placement, instagram_explore_placement])

post_likes_mobile = CatalogNode(Targeting.DevicePlatforms.mobile,
                                [post_likes_mobile_facebook, post_likes_mobile_instagram])

post_likes_desktop_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook,
                                          [facebook_in_stream_videos_placement, facebook_feed_placement,
                                           facebook_video_feeds_placement, facebook_marketplace_placement,
                                           facebook_search_results_placement])

post_likes_desktop = CatalogNode(Targeting.DevicePlatforms.desktop,
                                 [post_likes_desktop_facebook])

post_likes_placement_catalog = copy.deepcopy(post_likes)
post_likes_placement_catalog.children = [post_likes_mobile, post_likes_desktop]