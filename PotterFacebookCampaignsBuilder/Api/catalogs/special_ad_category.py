from facebook_business.adobjects.campaign import Campaign

from PotterFacebookCampaignsBuilder.Api.catalogs.base import Base
from PotterFacebookCampaignsBuilder.Api.catalogs.node import Node

_category = Campaign.SpecialAdCategory


class SpecialAdCategory(Base):
    A_credit = Node(_category.credit)
    B_housing = Node(_category.housing)
    C_employment = Node(_category.employment)
