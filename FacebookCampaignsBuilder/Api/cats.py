from Core.facebook.sdk_adapter.ad_objects.ad_account_matched_search_applications_edge_data import AppStore
from Core.facebook.sdk_adapter.ad_objects.ad_campaign_delivery_estimate import OptimizationGoal
from Core.facebook.sdk_adapter.ad_objects.ad_creative import ApplinkTreatment, CallToActionType
from Core.facebook.sdk_adapter.ad_objects.ad_insights import ActionAttributionWindows
from Core.facebook.sdk_adapter.ad_objects.ad_place_page_set import LocationTypeGroup, LocationType
from Core.facebook.sdk_adapter.ad_objects.ad_preview import AdFormat
from Core.facebook.sdk_adapter.ad_objects.ad_set import BillingEvent, PacingType, DestinationType
from Core.facebook.sdk_adapter.ad_objects.campaign import BidStrategy, Objective, SpecialAdCategories, ObjectiveWithDestination, ObjectiveWithDestinationGroup
from Core.facebook.sdk_adapter.ad_objects.content_delivery_report import Platform, Position, Placement
from Core.facebook.sdk_adapter.ad_objects.gender import Gender
from Core.facebook.sdk_adapter.ad_objects.product_event_stat import DeviceType
from Core.facebook.sdk_adapter.ad_objects.reach_frequency_prediction import BuyingType
from Core.facebook.sdk_adapter.ad_objects.targeting import DevicePlatform


catalogs = [
    # === [ I ] Campaign ===
    ObjectiveWithDestinationGroup,
    ObjectiveWithDestination,
    Objective,
    SpecialAdCategories,  # on/off
    # == Campaign budget optimization ==
    # TODO: lifetime vs daily budget
    # TODO: suggested budget - default int value
    BidStrategy,
    PacingType,
    # TODO: not in wireframes currently, but perhaps necessary
    OptimizationGoal,
    BillingEvent,
    BuyingType,
    # === [ II ] Ad set ===
    # TODO: see if Identity / Destination is DestinationType
    DestinationType,
    # == Placement ==
    Placement,
    Platform,
    Position,
    # == Targeting ==
    Gender,
    #  Age: ??? int range/enum ???
    #  Location: API
    #  Languages: API
    #  Interests: include / exclude [exclude / narrow]
    # Date ???
    # Ad set Budget Optimization == Campaign Budget Optimization
    # === Ad ===
    # Media format: video, image, carousel ???collection???
    # ??? adcreative.ObjectType adcreative.CategoryMediaSource
    # adimage.AdImage
    # advideo.AdVideo
    # == [ III ] Ad creation ==
    CallToActionType,  # NONE is an option
    AdFormat,
    DevicePlatform,
    DeviceType,
    # Media URL
    # Primary text
    # Headline
    # Description
    # Website URL
    # Display link [optional]
    # == Tracking == (pixel)
    # Facebook Pixel on/off
    # App Events on/off
    # == Conversion Events == multi-column drop down
    # ? active / inactive
    # ? view / add to cart
    # ? int
    # == Dynamic Ads ==
    # ? first in list
    # == [ IV ] Breakdowns ==
    # ?
    # === UNASSIGNED ===
    AppStore,
    ApplinkTreatment,
    ActionAttributionWindows,
    LocationTypeGroup,
    LocationType,
]
