from facebook_business.adobjects.campaign import Campaign

from FacebookCampaignsBuilder.Api.catalogs.base import Base
from FacebookCampaignsBuilder.Api.catalogs.node import Node

_category = Campaign.SpecialAdCategory


class SpecialAdCategory(Base):
    A_credit = Node(_category.credit)
    B_housing = Node(_category.housing)
    C_employment = Node(_category.employment)
