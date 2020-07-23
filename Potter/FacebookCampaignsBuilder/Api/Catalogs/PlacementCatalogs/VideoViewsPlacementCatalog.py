import copy
from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport
from facebook_business.adobjects.targeting import Targeting
from Potter.FacebookCampaignsBuilder.Api.Catalogs.ObjectivesCatalog import video_views
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.Placements import facebook_feed_placement, \
    facebook_instant_article_placement, facebook_stories_placement, facebook_marketplace_placement, \
    facebook_in_stream_videos_placement, facebook_video_feeds_placement, facebook_search_results_placement, \
    instagram_feed_placement, instagram_explore_placement, instagram_stories_placement, \
    audience_network_native_placement, audience_network_rewarded_videos_placement, \
    audience_network_in_stream_videos_placement

video_views_mobile_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook, 'Facebook', 'facebook-placement',
                                          None,
                                          [facebook_feed_placement, facebook_instant_article_placement,
                                           facebook_marketplace_placement, facebook_stories_placement,
                                           facebook_in_stream_videos_placement, facebook_video_feeds_placement,
                                           facebook_search_results_placement])

video_views_mobile_instagram = CatalogNode(ContentDeliveryReport.Platform.instagram, 'Instagram', 'instagram-placement',
                                           None,
                                           [instagram_feed_placement, instagram_stories_placement,
                                            instagram_explore_placement])

video_views_mobile_audience_network = CatalogNode(ContentDeliveryReport.Platform.audience_network, 'Apps & Sites',
                                                  'apps-placement', None, [audience_network_native_placement,
                                                                           audience_network_rewarded_videos_placement,
                                                                           audience_network_in_stream_videos_placement])

video_views_mobile = CatalogNode(Targeting.DevicePlatforms.mobile, 'Mobile', None, None,
                                 [video_views_mobile_facebook, video_views_mobile_instagram,
                                  video_views_mobile_audience_network])

video_views_desktop_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook, 'Facebook', 'facebook-placement',
                                           None,
                                           [facebook_feed_placement, facebook_marketplace_placement,
                                            facebook_in_stream_videos_placement, facebook_video_feeds_placement,
                                            facebook_search_results_placement
                                            ])

video_views_desktop_audience_network = CatalogNode(ContentDeliveryReport.Platform.audience_network, 'Apps & Sites',
                                                   'apps-placement', None,
                                                   [audience_network_in_stream_videos_placement,
                                                    audience_network_native_placement,
                                                    audience_network_rewarded_videos_placement])

video_views_desktop = CatalogNode(Targeting.DevicePlatforms.desktop, 'Desktop', None, None,
                                  [video_views_desktop_facebook, video_views_desktop_audience_network])

video_views_placement_catalog = copy.deepcopy(video_views)
video_views_placement_catalog.display_name = None
video_views_placement_catalog.description = None
video_views_placement_catalog.image_name = None
video_views_placement_catalog.children = [video_views_mobile, video_views_desktop]