from facebook_business.adobjects.campaign import Campaign

from FacebookCampaignsBuilder.Api.catalogs.base import Base
from FacebookCampaignsBuilder.Api.catalogs.node import Node


class SpecialAdCategories(Base):
    credit = Node(Campaign.SpecialAdCategories.credit)
    housing = Node(Campaign.SpecialAdCategories.housing)
    employment = Node(Campaign.SpecialAdCategories.employment)
