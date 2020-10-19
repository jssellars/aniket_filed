from facebook_business.adobjects.campaign import Campaign

from Potter.FacebookCampaignsBuilder.Api.catalogs.base import Base
from Potter.FacebookCampaignsBuilder.Api.catalogs.node import Node


class SpecialAdCategory(Base):
    A_credit = Node(Campaign.SpecialAdCategory.credit)
    B_housing = Node(Campaign.SpecialAdCategory.housing)
    C_employment = Node(Campaign.SpecialAdCategory.employment)
