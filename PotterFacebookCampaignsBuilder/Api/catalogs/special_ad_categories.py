from facebook_business.adobjects.campaign import Campaign

from PotterFacebookCampaignsBuilder.Api.catalogs.base import Base
from PotterFacebookCampaignsBuilder.Api.catalogs.node import Node


class SpecialAdCategories(Base):
    A_credit = Node(Campaign.SpecialAdCategories.credit)
    B_housing = Node(Campaign.SpecialAdCategories.housing)
    C_employment = Node(Campaign.SpecialAdCategories.employment)
