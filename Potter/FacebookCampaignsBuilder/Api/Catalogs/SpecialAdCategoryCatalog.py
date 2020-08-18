from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogBase import CatalogBase
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from facebook_business.adobjects.campaign import Campaign


class SpecialAdCategoryCatalog(CatalogBase):
    A_credit = CatalogNode(Campaign.SpecialAdCategory.credit)
    B_housing = CatalogNode(Campaign.SpecialAdCategory.housing)
    C_employment = CatalogNode(Campaign.SpecialAdCategory.employment)
