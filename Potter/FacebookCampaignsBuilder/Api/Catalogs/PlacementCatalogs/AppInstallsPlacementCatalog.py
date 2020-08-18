import copy

from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport
from facebook_business.adobjects.targeting import Targeting

from Potter.FacebookCampaignsBuilder.Api.Catalogs.ObjectivesCatalog import app_installs
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.Placements import facebook_feed_placement, \
    facebook_video_feeds_placement, facebook_stories_placement, facebook_instant_article_placement, \
    instagram_feed_placement, instagram_explore_placement, instagram_stories_placement, \
    audience_network_native_placement, audience_network_rewarded_videos_placement

app_installs_mobile_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook,
                                            [facebook_feed_placement, facebook_video_feeds_placement,
                                             facebook_instant_article_placement, facebook_stories_placement])
app_installs_mobile_instagram = CatalogNode(ContentDeliveryReport.Platform.instagram,
                                            [instagram_feed_placement, instagram_stories_placement, instagram_explore_placement])
app_installs_mobile_audience_network = CatalogNode(ContentDeliveryReport.Platform.audience_network,
                                                   [audience_network_native_placement,
                                                    audience_network_rewarded_videos_placement])

app_installs_mobile = CatalogNode(Targeting.DevicePlatforms.mobile,
                                  [app_installs_mobile_facebook, app_installs_mobile_instagram,
                                   app_installs_mobile_audience_network])


app_installs_desktop_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook,
                                            [facebook_feed_placement, facebook_video_feeds_placement,
                                             ])
app_installs_desktop = CatalogNode(Targeting.DevicePlatforms.desktop,
                                   [app_installs_desktop_facebook])

app_installs_placement_catalog = copy.deepcopy(app_installs)
app_installs_placement_catalog.children = [app_installs_mobile, app_installs_desktop]
