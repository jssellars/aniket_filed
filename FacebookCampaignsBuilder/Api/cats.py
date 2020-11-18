from Core.facebook.sdk_adapter.ad_objects.ad_account_matched_search_applications_edge_data import AppStore
from Core.facebook.sdk_adapter.ad_objects.ad_campaign_delivery_estimate import OptimizationGoal
from Core.facebook.sdk_adapter.ad_objects.ad_creative import ApplinkTreatment, CallToActionType
from Core.facebook.sdk_adapter.ad_objects.ad_insights import ActionAttributionWindowClick, ActionAttributionWindowView
from Core.facebook.sdk_adapter.ad_objects.ad_place_page_set import LocationTypeGroup, LocationType
from Core.facebook.sdk_adapter.ad_objects.ad_preview import AdFormat
from Core.facebook.sdk_adapter.ad_objects.ad_set import BillingEvent, PacingType, DestinationType
from Core.facebook.sdk_adapter.ad_objects.campaign import BidStrategy, Objective, SpecialAdCategories, \
    ObjectiveWithDestination, ObjectiveWithDestinationGroup, BudgetTimespan
from Core.facebook.sdk_adapter.ad_objects.content_delivery_report import Platform, Position, Placement
from Core.facebook.sdk_adapter.ad_objects.gender import Gender, GenderGroup
from Core.facebook.sdk_adapter.ad_objects.product_event_stat import DeviceType
from Core.facebook.sdk_adapter.ad_objects.reach_frequency_prediction import BuyingType
from Core.facebook.sdk_adapter.ad_objects.targeting import DevicePlatform


# Campaign creation params
#
#     'adlabels':                     'list<Object>',
#     'execution_options':            'list<execution_options_enum>',
#     'iterative_split_test_configs': 'list<Object>',
#     'promoted_object':              'Object',
#     'smart_promotion_type':         'smart_promotion_type_enum',
#     'source_campaign_id':           'string',
#     'status':                       'status_enum',
#     'topline_id':                   'string',
#     'upstream_events':              'map',

CATS = [
    # === [ I ] Campaign ===
    # Campaign name: 'name': 'string'
    ObjectiveWithDestinationGroup,
    ObjectiveWithDestination,
    Objective,  # 'objective': 'objective_enum'
    DestinationType,  # TODO: this should be used but no param found
    SpecialAdCategories,  # additional show/hide state, ??? multi-select -> later ???
    # 'special_ad_categories': 'list<special_ad_categories_enum>'
    # 'special_ad_category_country':  'list<special_ad_category_country_enum>'
    # == Campaign budget optimization ==
    BudgetTimespan,  # 'daily_budget': 'unsigned int' + 'lifetime_budget': 'unsigned int'
    # 'spend_cap': 'unsigned int'
    # TODO: suggested budget - default int value
    BidStrategy,  # only lowest cost  # 'bid_strategy': 'bid_strategy_enum'
    PacingType,  # only standard  # 'pacing_type': 'list<string>'
    # TODO: not in wireframes currently, but perhaps necessary
    OptimizationGoal,
    BillingEvent,
    BuyingType,  # only auction  # 'buying_type': 'string'
    # === [ II ] Ad set ===
    # TODO: see if Identity / Destination is DestinationType
    DestinationType,
    # == Placement ==
    Placement,
    Platform,
    Position,
    # == Targeting ==
    Gender,
    GenderGroup,
    #  Age: ??? int range/enum ???
    #  Location: API
    #  Languages: API
    #  Interests: include / exclude [exclude / narrow]
    # Date ???
    # Ad set Budget Optimization == Campaign Budget Optimization
    # === [ III ] Ad ===
    # Media format: video, image, carousel ???collection???
    # ??? adcreative.ObjectType adcreative.CategoryMediaSource
    # adimage.AdImage
    # advideo.AdVideo
    # == Ad creation ==
    CallToActionType,  # NONE is an option ??? NO_BUTTON ???
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
    # to be explored
    # === UNASSIGNED ===
    AppStore,
    ApplinkTreatment,
    ActionAttributionWindowClick,
    ActionAttributionWindowView,
    LocationTypeGroup,
    LocationType,
]
