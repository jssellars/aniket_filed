from enum import Enum

from facebook_business.adobjects.reachfrequencyprediction import ReachFrequencyPrediction

from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum

# https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group
# https://developers.facebook.com/docs/marketing-api/reachandfrequency
#
# Default value: AUCTION
# This field will help Facebook make optimizations to delivery, pricing, and limits.
# All ad sets in this campaign must match the buying type. Possible values are:
#   AUCTION (default)
#   RESERVED (for reach and frequency ads).

_buying_type = ReachFrequencyPrediction.BuyingType


@cat_enum
class BuyingType(Enum):
    AUCTION = Cat(_buying_type.auction)
    FIXED_CPM = Cat(_buying_type.fixed_cpm)
    MIXED = Cat(_buying_type.mixed)
    REACHBLOCK = Cat(_buying_type.reachblock)
    RESEARCH_POLL = Cat(_buying_type.research_poll)
    RESERVED = Cat(_buying_type.reserved)
