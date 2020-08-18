import copy
from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport
from facebook_business.adobjects.targeting import Targeting
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.Placements import facebook_in_stream_videos_placement, \
    facebook_search_results_placement, facebook_video_feeds_placement, facebook_marketplace_placement, \
    facebook_stories_placement, facebook_feed_placement, facebook_instant_article_placement

from Potter.FacebookCampaignsBuilder.Api.Catalogs.ObjectivesCatalog import page_likes


page_likes_mobile_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook,
                                         [facebook_in_stream_videos_placement, facebook_marketplace_placement,
                                          facebook_search_results_placement, facebook_video_feeds_placement,
                                          facebook_feed_placement, facebook_stories_placement,
                                          facebook_instant_article_placement])
page_likes_mobile = CatalogNode(Targeting.DevicePlatforms.mobile,
                                [page_likes_mobile_facebook])

page_likes_desktop_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook,
                                          [facebook_in_stream_videos_placement, facebook_feed_placement,
                                           facebook_search_results_placement, facebook_marketplace_placement,
                                           facebook_video_feeds_placement])

page_likes_desktop = CatalogNode(Targeting.DevicePlatforms.desktop,
                                 [page_likes_desktop_facebook])

page_likes_placement_catalog = copy.deepcopy(page_likes)
page_likes_placement_catalog.children = [page_likes_mobile, page_likes_desktop]