import copy
from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport
from facebook_business.adobjects.targeting import Targeting

from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.Placements import facebook_in_stream_videos_placement, \
    facebook_stories_placement, facebook_marketplace_placement, facebook_feed_placement, facebook_video_feeds_placement, \
    facebook_instant_article_placement, facebook_search_results_placement

from Potter.FacebookCampaignsBuilder.Api.Catalogs.ObjectivesCatalog import store_traffic

store_traffic_mobile_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook, 'Facebook', 'facebook-placement', None,
                                            [facebook_in_stream_videos_placement, facebook_marketplace_placement, facebook_stories_placement,
                                             facebook_instant_article_placement, facebook_feed_placement, facebook_video_feeds_placement,
                                             facebook_search_results_placement])


store_traffic_mobile = CatalogNode(Targeting.DevicePlatforms.mobile, 'Mobile', None, None,
                                   [store_traffic_mobile_facebook])

store_traffic_desktop_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook, 'Facebook', 'facebook-placement', None,
                                             [facebook_feed_placement,
                                              facebook_search_results_placement,
                                              facebook_marketplace_placement,
                                              facebook_video_feeds_placement,
                                              facebook_in_stream_videos_placement])


store_traffic_desktop = CatalogNode(Targeting.DevicePlatforms.desktop, 'Desktop', None, None,
                                    [store_traffic_desktop_facebook])

store_traffic_placement_catalog = copy.deepcopy(store_traffic)
store_traffic_placement_catalog.display_name = None
store_traffic_placement_catalog.description = None
store_traffic_placement_catalog.image_name = None
store_traffic_placement_catalog.children = [store_traffic_mobile, store_traffic_desktop]
