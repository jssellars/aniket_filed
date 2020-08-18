import copy
from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport
from facebook_business.adobjects.targeting import Targeting
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from Potter.FacebookCampaignsBuilder.Api.Catalogs.ObjectivesCatalog import brand_awareness
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.Placements import facebook_feed_placement, \
    facebook_in_stream_videos_placement, facebook_video_feeds_placement, audience_network_native_placement, \
    audience_network_in_stream_videos_placement, instagram_feed_placement, facebook_stories_placement, \
    facebook_instant_article_placement

brand_awareness_mobile_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook,
                                              [facebook_feed_placement, facebook_video_feeds_placement,
                                               facebook_instant_article_placement, facebook_in_stream_videos_placement,
                                               facebook_stories_placement])

brand_awareness_mobile_instagram = CatalogNode(ContentDeliveryReport.Platform.instagram,
                                               [instagram_feed_placement])

brand_awareness_mobile_audience_network = CatalogNode(ContentDeliveryReport.Platform.audience_network,
                                                      [audience_network_native_placement,
                                                       audience_network_in_stream_videos_placement])

brand_awareness_mobile = CatalogNode(Targeting.DevicePlatforms.mobile,
                                     [brand_awareness_mobile_facebook,
                                      brand_awareness_mobile_instagram,
                                      brand_awareness_mobile_audience_network])

brand_awareness_desktop_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook,
                                               [facebook_feed_placement, facebook_video_feeds_placement,
                                                facebook_in_stream_videos_placement])

brand_awareness_desktop_audience_network = CatalogNode(ContentDeliveryReport.Platform.audience_network,
                                                       [audience_network_native_placement,
                                                        audience_network_in_stream_videos_placement])

brand_awareness_desktop = CatalogNode(Targeting.DevicePlatforms.desktop,
                                      [brand_awareness_desktop_facebook, brand_awareness_desktop_audience_network])

brand_awareness_placement_catalog = copy.deepcopy(brand_awareness)
brand_awareness_placement_catalog.children = [brand_awareness_mobile, brand_awareness_desktop]