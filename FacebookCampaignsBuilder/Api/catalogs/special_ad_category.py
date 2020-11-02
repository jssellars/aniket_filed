from facebook_business.adobjects.campaign import Campaign

from FacebookCampaignsBuilder.Api.catalogs.base import Base
from FacebookCampaignsBuilder.Api.catalogs.node import Node

_category = Campaign.SpecialAdCategory


class SpecialAdCategory(Base):
    credit = Node(_category.credit)
    housing = Node(_category.housing)
    employment = Node(_category.employment)
