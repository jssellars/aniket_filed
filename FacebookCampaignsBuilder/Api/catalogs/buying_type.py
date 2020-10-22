from facebook_business.adobjects.reachfrequencyprediction import ReachFrequencyPrediction

from FacebookCampaignsBuilder.Api.catalogs.base import Base
from FacebookCampaignsBuilder.Api.catalogs.node import Node

# https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group
# https://developers.facebook.com/docs/marketing-api/reachandfrequency
#
# Default value: AUCTION
# This field will help Facebook make optimizations to delivery, pricing, and limits.
# All ad sets in this campaign must match the buying type. Possible values are:
#   AUCTION (default)
#   RESERVED (for reach and frequency ads).


_buying_type = ReachFrequencyPrediction.BuyingType


class BuyingType(Base):
    auction = Node(_buying_type.auction)
    fixed_cpm = Node(_buying_type.fixed_cpm)
    mixed = Node(_buying_type.mixed)
    reachblock = Node(_buying_type.reachblock)
    research_poll = Node(_buying_type.research_poll)
    reserved = Node(_buying_type.reserved)
