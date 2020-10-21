from facebook_business.adobjects.adcreative import AdCreative

from PotterFacebookCampaignsBuilder.Api.catalogs.base import Base
from PotterFacebookCampaignsBuilder.Api.catalogs.node import Node

# https://developers.facebook.com/docs/marketing-api/dynamic-product-ads/ads-management/#deep-link

_applink_treatment = AdCreative.ApplinkTreatment


class ApplinkTreatment(Base):
    deeplink_with_appstore_fallback = Node(_applink_treatment.deeplink_with_appstore_fallback)
    deeplink_with_web_fallback = Node(_applink_treatment.deeplink_with_web_fallback)
    web_only = Node(_applink_treatment.web_only)
