import copy
from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport
from facebook_business.adobjects.targeting import Targeting
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from Potter.FacebookCampaignsBuilder.Api.Catalogs.ObjectivesCatalog import reach
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.Placements import audience_network_rewarded_videos_placement, \
    audience_network_native_placement, audience_network_in_stream_videos_placement, facebook_feed_placement, \
    facebook_search_results_placement, facebook_video_feeds_placement, facebook_marketplace_placement, \
    facebook_in_stream_videos_placement, instagram_explore_placement, instagram_feed_placement, \
    instagram_stories_placement, facebook_stories_placement, facebook_instant_article_placement

reach_mobile_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook,
                                    [facebook_in_stream_videos_placement, facebook_stories_placement,
                                     facebook_marketplace_placement,
                                     facebook_video_feeds_placement, facebook_instant_article_placement,
                                     facebook_feed_placement, facebook_search_results_placement])

reach_mobile_instagram = CatalogNode(ContentDeliveryReport.Platform.instagram,
                                     [instagram_feed_placement, instagram_stories_placement,
                                      instagram_explore_placement])

reach_mobile_audience_network = CatalogNode(ContentDeliveryReport.Platform.audience_network,
                                            [audience_network_in_stream_videos_placement,
                                             audience_network_rewarded_videos_placement,
                                             audience_network_native_placement])

reach_mobile = CatalogNode(Targeting.DevicePlatforms.mobile,
                           [reach_mobile_facebook, reach_mobile_instagram, reach_mobile_audience_network])

reach_desktop_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook,
                                     [facebook_in_stream_videos_placement,
                                      facebook_marketplace_placement,
                                      facebook_video_feeds_placement,
                                      facebook_feed_placement, facebook_search_results_placement
                                      ])

reach_desktop_audience_network = CatalogNode(ContentDeliveryReport.Platform.audience_network,
                                             [audience_network_in_stream_videos_placement,
                                              audience_network_native_placement,
                                              audience_network_rewarded_videos_placement])

reach_desktop = CatalogNode(Targeting.DevicePlatforms.desktop,
                            [reach_desktop_facebook, reach_desktop_audience_network])

reach_placement_catalog = copy.deepcopy(reach)
reach_placement_catalog.children = [reach_mobile, reach_desktop]