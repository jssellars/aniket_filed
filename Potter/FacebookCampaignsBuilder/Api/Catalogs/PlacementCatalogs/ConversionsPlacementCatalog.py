import copy

from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport
from facebook_business.adobjects.targeting import Targeting

from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from Potter.FacebookCampaignsBuilder.Api.Catalogs.ObjectivesCatalog import conversions_leaf
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.Placements import facebook_feed_placement, \
    facebook_instant_article_placement, facebook_marketplace_placement, facebook_in_stream_videos_placement, \
    facebook_right_column_placement, facebook_search_results_placement, facebook_stories_placement, \
    facebook_video_feeds_placement, instagram_feed_placement, instagram_stories_placement, instagram_explore_placement, \
    audience_network_native_placement, audience_network_in_stream_videos_placement, \
    audience_network_rewarded_videos_placement

conversions_mobile_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook, 'Facebook', 'facebook-placement',
                                          None,
                                          [facebook_feed_placement, facebook_instant_article_placement,
                                           facebook_video_feeds_placement, facebook_marketplace_placement,
                                           facebook_stories_placement, facebook_in_stream_videos_placement,
                                           facebook_search_results_placement, facebook_right_column_placement])

conversions_mobile_instagram = CatalogNode(ContentDeliveryReport.Platform.instagram, 'Instagram',
                                           'instagram-placement', None,
                                           [instagram_feed_placement, instagram_stories_placement,
                                            instagram_explore_placement])

conversions_mobile = CatalogNode(Targeting.DevicePlatforms.mobile, 'Mobile', None, None,
                                 [conversions_mobile_facebook, conversions_mobile_instagram])

conversions_desktop_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook, 'Facebook', 'facebook-placement',
                                           None,
                                           [facebook_feed_placement, facebook_video_feeds_placement,
                                            facebook_right_column_placement, facebook_search_results_placement,
                                            facebook_in_stream_videos_placement, facebook_marketplace_placement])

conversions_desktop_audience_network = CatalogNode(ContentDeliveryReport.Platform.audience_network, 'Apps & Sites',
                                                   'apps-placement', None,
                                                   [audience_network_native_placement,
                                                    audience_network_in_stream_videos_placement,
                                                    audience_network_rewarded_videos_placement])

conversions_desktop = CatalogNode(Targeting.DevicePlatforms.desktop, 'Desktop', None, None,
                                  [conversions_desktop_facebook, conversions_desktop_audience_network])

conversions_placement_catalog = copy.deepcopy(conversions_leaf)
conversions_placement_catalog.display_name = None
conversions_placement_catalog.description = None
conversions_placement_catalog.image_name = None
conversions_placement_catalog.children = [conversions_mobile, conversions_desktop]