import copy
from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport
from facebook_business.adobjects.targeting import Targeting
from Potter.FacebookCampaignsBuilder.Api.Catalogs.ObjectivesCatalog import lead_generation
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.Placements import facebook_feed_placement, facebook_stories_placement, \
    instagram_feed_placement

lead_generation_mobile_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook, 'Facebook', 'facebook-placement',
                                              None,
                                              [facebook_feed_placement,
                                               facebook_stories_placement
                                               ])

lead_generation_mobile_instagram = CatalogNode(ContentDeliveryReport.Platform.instagram, 'Instagram',
                                               'instagram-placement', None,
                                               [instagram_feed_placement])

lead_generation_mobile = CatalogNode(Targeting.DevicePlatforms.mobile, 'Mobile', None, None,
                                     [lead_generation_mobile_facebook, lead_generation_mobile_instagram])

lead_generation_desktop_facebook = CatalogNode(ContentDeliveryReport.Platform.facebook, 'Facebook',
                                               'facebook-placement',
                                               None,
                                               [facebook_feed_placement])

lead_generation_desktop = CatalogNode(Targeting.DevicePlatforms.desktop, 'Desktop', None, None,
                                      [lead_generation_desktop_facebook])

lead_generation_placement_catalog = copy.deepcopy(lead_generation)
lead_generation_placement_catalog.display_name = None
lead_generation_placement_catalog.description = None
lead_generation_placement_catalog.image_name = None
lead_generation_placement_catalog.children = [lead_generation_mobile, lead_generation_desktop]