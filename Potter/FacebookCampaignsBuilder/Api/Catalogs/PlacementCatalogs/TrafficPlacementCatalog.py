import copy
from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport
from facebook_business.adobjects.targeting import Targeting
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.Placements import facebook_feed_placement, \
    facebook_instant_article_placement, facebook_right_column_placement, facebook_video_feeds_placement, \
    facebook_marketplace_placement, facebook_stories_placement, facebook_search_results_placement, \
    facebook_in_stream_videos_placement, instagram_feed_placement, instagram_stories_placement, \
    instagram_explore_placement, audience_network_native_placement, audience_network_in_stream_videos_placement, \
    audience_network_rewarded_videos_placement
from Potter.FacebookCampaignsBuilder.Api.Catalogs.ObjectivesCatalog import website_traffic

traffic_mobile_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook,
                                      [facebook_feed_placement, facebook_instant_article_placement,
                                       facebook_video_feeds_placement, facebook_right_column_placement,
                                       facebook_marketplace_placement, facebook_stories_placement,
                                       facebook_in_stream_videos_placement, facebook_search_results_placement])

traffic_mobile_instagram = CatalogNode(ContentDeliveryReport.Platform.instagram,
                                       [instagram_feed_placement, instagram_stories_placement,
                                        instagram_explore_placement])

traffic_mobile_audience_network = CatalogNode(ContentDeliveryReport.Platform.audience_network,
                                              [audience_network_native_placement,
                                               audience_network_in_stream_videos_placement,
                                               audience_network_rewarded_videos_placement])

traffic_mobile = CatalogNode(Targeting.DevicePlatforms.mobile,
                             [traffic_mobile_facebook, traffic_mobile_instagram, traffic_mobile_audience_network])

traffic_desktop_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook,
                                       [facebook_feed_placement, facebook_marketplace_placement,
                                        facebook_in_stream_videos_placement, facebook_right_column_placement,
                                        facebook_search_results_placement, facebook_video_feeds_placement])

traffic_desktop_audience_network = CatalogNode(ContentDeliveryReport.Platform.audience_network,
                                               [audience_network_native_placement,
                                                audience_network_in_stream_videos_placement,
                                                audience_network_rewarded_videos_placement])

traffic_desktop = CatalogNode(Targeting.DevicePlatforms.desktop,
                              [traffic_desktop_facebook, traffic_desktop_audience_network])

traffic_placement_catalog = copy.deepcopy(website_traffic)
traffic_placement_catalog.children = [traffic_mobile, traffic_desktop]
