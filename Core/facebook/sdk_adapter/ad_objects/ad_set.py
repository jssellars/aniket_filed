from enum import Enum

from facebook_business.adobjects.adset import AdSet

from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum

# https://developers.facebook.com/docs/marketing-api/bidding/overview/billing-events/#buying-type-validation

_billing_event = AdSet.BillingEvent


@cat_enum
class BillingEvent(Enum):
    APP_INSTALLS = Cat(_billing_event.app_installs)
    CLICKS = Cat(_billing_event.clicks)
    IMPRESSIONS = Cat(_billing_event.impressions)
    LINK_CLICKS = Cat(_billing_event.link_clicks)
    OFFER_CLAIMS = Cat(_billing_event.offer_claims)
    PAGE_LIKES = Cat(_billing_event.page_likes)
    POST_ENGAGEMENT = Cat(_billing_event.post_engagement)
    THRUPLAY = Cat(_billing_event.thruplay)


# https://developers.facebook.com/docs/marketing-api/bidding/overview/pacing-and-scheduling
# https://developers.facebook.com/docs/marketing-api/adset/pacing
# standard
#   Default pacing mechanism
# day_parting
#   Used for an ad set that has delivery schedule (Ad Scheduling)
# no_pacing
#   No pacing - accelerated delivery
# disabled
#   Pacing is disabled by default for impressions-paced bid type (Reach & Frequency) ad sets


@cat_enum
class PacingType(Enum):
    STANDARD = Cat("standard")
    DAY_PARTING = Cat("day_parting")
    NO_PACING = Cat("no_pacing")
    DISABLED = Cat("disabled")


# https://developers.facebook.com/docs/marketing-api/adset/destination_type

_destination_type = AdSet.DestinationType


@cat_enum
class DestinationType(Enum):
    APP = Cat(_destination_type.app)
    APPLINKS_AUTOMATIC = Cat(_destination_type.applinks_automatic)
    FACEBOOK = Cat(_destination_type.facebook)
    MESSENGER = Cat(_destination_type.messenger)
    UNDEFINED = Cat(_destination_type.undefined)
    WEBSITE = Cat(_destination_type.website)
