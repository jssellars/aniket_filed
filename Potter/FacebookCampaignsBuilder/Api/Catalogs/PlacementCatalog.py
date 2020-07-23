from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.AppInstallsPlacementCatalog import \
    app_installs_placement_catalog
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.BrandAwarenessPlacementCatalog import \
    brand_awareness_placement_catalog
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.CatalogSalesPlacementCatalog import \
    catalog_sales_placement_catalog
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.ConversionsPlacementCatalog import \
    conversions_placement_catalog
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.PageLikesPlacementCatalog import \
    page_likes_placement_catalog
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.PostLikesPlacementCatalog import \
    post_likes_placement_catalog
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.ReachPlacementCatalog import reach_placement_catalog
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.StoreTrafficPlacementCatalog import \
    store_traffic_placement_catalog
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.TrafficPlacementCatalog import \
    traffic_placement_catalog
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.VideoViewsPlacementCatalog import \
    video_views_placement_catalog
from Potter.FacebookCampaignsBuilder.Api.Catalogs.PlacementCatalogs.LeadGenerationPlacementCatalog import \
    lead_generation_placement_catalog

from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogBase import CatalogBase


class PlacementCatalog(CatalogBase):
    A_brand_awareness = brand_awareness_placement_catalog
    B_reach = reach_placement_catalog
    C_traffic = traffic_placement_catalog
    D_video_views = video_views_placement_catalog
    E_lead_generation = lead_generation_placement_catalog
    F_conversions = conversions_placement_catalog
    G_catalog_sales = catalog_sales_placement_catalog
    F_post_likes = post_likes_placement_catalog
    H_page_likes = page_likes_placement_catalog
    I_app_installs = app_installs_placement_catalog
    J_store_traffic = store_traffic_placement_catalog

