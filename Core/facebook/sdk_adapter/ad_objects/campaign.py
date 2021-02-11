from enum import Enum

from facebook_business.adobjects.campaign import Campaign

from Core.facebook.sdk_adapter.ad_objects.ad_set import DestinationType
from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum, Contexts

# TODO: add documentation link(s)

_special_ad_category = Campaign.SpecialAdCategories


@cat_enum
class SpecialAdCategories(Enum):
    CREDIT = Cat(_special_ad_category.credit)
    EMPLOYMENT = Cat(_special_ad_category.employment)
    HOUSING = Cat(_special_ad_category.housing)
    NONE = Cat(_special_ad_category.none)

    contexts = Contexts.all_with_items(CREDIT, EMPLOYMENT, HOUSING, NONE, default_item=NONE)


# https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group#parameters-2
# https://www.facebook.com/business/help/1438417719786914

_objective = Campaign.Objective


@cat_enum
class Objective(Enum):
    APP_INSTALLS = Cat(
        _objective.app_installs, description="Send people to the store where they can download your business's app.",
    )
    BRAND_AWARENESS = Cat(
        _objective.brand_awareness, description="Increase people's awareness of your business, brand or service.",
    )
    CONVERSIONS = Cat(
        _objective.conversions,
        description="Encourage people to take a specific action on your business's site, such as having them to add items to a cart, download your app, register for your site, or make a purchase.",
    )
    EVENT_RESPONSES = Cat(_objective.event_responses)
    LEAD_GENERATION = Cat(
        _objective.lead_generation,
        description="Collect leads for your business. Create ads that collect info from people interested in your product, such as sign-ups for newsletters.",
    )
    LINK_CLICKS = Cat(
        _objective.link_clicks,
        display_name="Traffic",
        description="Send people from Facebook to any URL you choose, such as your website's landing page, a blog post, app etc.",
    )
    LOCAL_AWARENESS = Cat(_objective.local_awareness, display_name="Store Traffic")
    MESSAGES = Cat(
        _objective.messages,
        description="Connect with people on Messenger, Instagram Direct, and WhatsApp. Communicate with potential or existing customers to encourage interest in your business.",
    )
    OFFER_CLAIMS = Cat(_objective.offer_claims)
    # ENGAGEMENT = [PAGE_LIKES, POST_ENGAGEMENT]
    #     Reach people more likely to engage with your post.
    #     Engagement includes likes, comments and shares but can also include offers claimed from your page.
    PAGE_LIKES = Cat(
        _objective.page_likes,
        display_name="Engagement - Page Likes",
        description="Reach people more likely to engage with your page.",
    )
    POST_ENGAGEMENT = Cat(
        _objective.post_engagement,
        display_name="Engagement - Post Likes",
        description="Reach people more likely to engage with your post.",
    )
    PRODUCT_CATALOG_SALES = Cat(
        _objective.product_catalog_sales,
        display_name="Catalog Sales",
        description="Show products from your ecommerce store's catalog to generate sales.",
    )
    REACH = Cat(_objective.reach, description="Show your ad to as many people as possible in your target audience.",)
    VIDEO_VIEWS = Cat(
        _objective.video_views,
        description="Share videos of your business with people on Facebook most likely to watch it.",
    )

    STORE_VISITS = Cat(
        "STORE_VISITS", description="Promote your brick-and-mortar business locations to people that are nearby.",
    )


@cat_enum
class ObjectiveWithDestination(Enum):
    APP_INSTALLS_X_UNDEFINED = Cat(None, Objective.APP_INSTALLS, DestinationType.UNDEFINED).with_metadata_from(
        Objective.APP_INSTALLS
    )
    APP_INSTALLS_X_APP = Cat(None, Objective.APP_INSTALLS, DestinationType.APP).with_metadata_from(
        Objective.APP_INSTALLS
    )
    BRAND_AWARENESS_X_UNDEFINED = Cat(None, Objective.BRAND_AWARENESS, DestinationType.UNDEFINED).with_metadata_from(
        Objective.BRAND_AWARENESS
    )
    CONVERSIONS_X_UNDEFINED = Cat(None, Objective.CONVERSIONS, DestinationType.UNDEFINED).with_metadata_from(
        Objective.CONVERSIONS
    )
    CONVERSIONS_X_WEBSITE = Cat(
        None,
        Objective.CONVERSIONS,
        DestinationType.WEBSITE,
        display_name="Website Conversions",
        description="Encourage people to take a specific action on your business's site, such as having them to add items to a cart, register for your site, or make a purchase.",
    )
    CONVERSIONS_X_APP = Cat(
        None,
        Objective.CONVERSIONS,
        DestinationType.APP,
        display_name="App Conversions",
        description="Encourage people to take a specific action on your business's site, such as having them download your app.",
    )
    CONVERSIONS_X_MESSENGER = Cat(None, Objective.CONVERSIONS, DestinationType.MESSENGER)
    CONVERSIONS_X_APPLINKS_AUTOMATIC = Cat(None, Objective.CONVERSIONS, DestinationType.APPLINKS_AUTOMATIC)
    EVENT_RESPONSES_X_UNDEFINED = Cat(None, Objective.EVENT_RESPONSES, DestinationType.UNDEFINED).with_metadata_from(
        Objective.EVENT_RESPONSES
    )
    LEAD_GENERATION_X_UNDEFINED = Cat(None, Objective.LEAD_GENERATION, DestinationType.UNDEFINED).with_metadata_from(
        Objective.LEAD_GENERATION
    )
    LINK_CLICKS_X_UNDEFINED = Cat(None, Objective.LINK_CLICKS, DestinationType.UNDEFINED).with_metadata_from(
        Objective.LINK_CLICKS
    )
    LINK_CLICKS_X_WEBSITE = Cat(
        None,
        Objective.LINK_CLICKS,
        DestinationType.WEBSITE,
        display_name="Website Traffic",
        description="Send people from Facebook to the URL of your website's landing page.",
    )
    LINK_CLICKS_X_APP = Cat(
        None,
        Objective.LINK_CLICKS,
        DestinationType.APP,
        display_name="App Traffic",
        description="Send people from Facebook to the URL of your app.",
    )
    LINK_CLICKS_X_MESSENGER = Cat(None, Objective.LINK_CLICKS, DestinationType.MESSENGER)
    LINK_CLICKS_X_APPLINKS_AUTOMATIC = Cat(None, Objective.LINK_CLICKS, DestinationType.APPLINKS_AUTOMATIC)
    LOCAL_AWARENESS_X_UNDEFINED = Cat(None, Objective.LOCAL_AWARENESS, DestinationType.UNDEFINED).with_metadata_from(
        Objective.LOCAL_AWARENESS
    )
    MESSAGES_X_UNDEFINED = Cat(None, Objective.MESSAGES, DestinationType.UNDEFINED).with_metadata_from(
        Objective.MESSAGES
    )
    OFFER_CLAIMS_X_UNDEFINED = Cat(None, Objective.OFFER_CLAIMS, DestinationType.UNDEFINED).with_metadata_from(
        Objective.OFFER_CLAIMS
    )
    PAGE_LIKES_X_UNDEFINED = Cat(None, Objective.PAGE_LIKES, DestinationType.UNDEFINED).with_metadata_from(
        Objective.PAGE_LIKES
    )
    POST_ENGAGEMENT_X_UNDEFINED = Cat(None, Objective.POST_ENGAGEMENT, DestinationType.UNDEFINED).with_metadata_from(
        Objective.POST_ENGAGEMENT
    )
    PRODUCT_CATALOG_SALES_X_UNDEFINED = Cat(
        None, Objective.PRODUCT_CATALOG_SALES, DestinationType.UNDEFINED
    ).with_metadata_from(Objective.PRODUCT_CATALOG_SALES)
    PRODUCT_CATALOG_SALES_X_APPLINKS_AUTOMATIC = Cat(
        None, Objective.PRODUCT_CATALOG_SALES, DestinationType.APPLINKS_AUTOMATIC
    )
    REACH_X_UNDEFINED = Cat(None, Objective.REACH, DestinationType.UNDEFINED).with_metadata_from(Objective.REACH)
    VIDEO_VIEWS_X_UNDEFINED = Cat(None, Objective.VIDEO_VIEWS, DestinationType.UNDEFINED).with_metadata_from(
        Objective.VIDEO_VIEWS
    )
    STORE_VISITS_X_UNDEFINED = Cat(None, Objective.STORE_VISITS, DestinationType.UNDEFINED).with_metadata_from(
        Objective.STORE_VISITS
    )

    joint_fields = [Objective, DestinationType]
    contexts = Contexts.all_with_items(
        APP_INSTALLS_X_UNDEFINED,
        BRAND_AWARENESS_X_UNDEFINED,
        CONVERSIONS_X_UNDEFINED,
        LEAD_GENERATION_X_UNDEFINED,
        LINK_CLICKS_X_WEBSITE,
        LINK_CLICKS_X_APP,
        PAGE_LIKES_X_UNDEFINED,
        POST_ENGAGEMENT_X_UNDEFINED,
        PRODUCT_CATALOG_SALES_X_UNDEFINED,
        REACH_X_UNDEFINED,
        VIDEO_VIEWS_X_UNDEFINED,
        default_item=BRAND_AWARENESS_X_UNDEFINED,
    )


@cat_enum
class ObjectiveWithDestinationGroup(Enum):
    APP_ACTIVITY = Cat(
        None,
        ObjectiveWithDestination.LINK_CLICKS_X_APP,
        ObjectiveWithDestination.APP_INSTALLS_X_UNDEFINED,
        ObjectiveWithDestination.CONVERSIONS_X_APP,
        # not yet supported
        # ObjectiveWithDestination.LOCAL_AWARENESS_X_UNDEFINED,
        default_item=ObjectiveWithDestination.LINK_CLICKS_X_APP,
    )
    AWARENESS = Cat(
        None,
        ObjectiveWithDestination.BRAND_AWARENESS_X_UNDEFINED,
        ObjectiveWithDestination.REACH_X_UNDEFINED,
        default_item=ObjectiveWithDestination.BRAND_AWARENESS_X_UNDEFINED,
    )
    CONSIDERATION = Cat(
        None,
        ObjectiveWithDestination.LINK_CLICKS_X_WEBSITE,
        # part of ENGAGEMENT
        ObjectiveWithDestination.PAGE_LIKES_X_UNDEFINED,
        # part of ENGAGEMENT
        ObjectiveWithDestination.POST_ENGAGEMENT_X_UNDEFINED,
        ObjectiveWithDestination.VIDEO_VIEWS_X_UNDEFINED,
        ObjectiveWithDestination.LEAD_GENERATION_X_UNDEFINED,
        # not yet supported
        # ObjectiveWithDestination.MESSAGES_X_UNDEFINED,
        default_item=ObjectiveWithDestination.LINK_CLICKS_X_WEBSITE,
    )
    CONVERSIONS = Cat(
        None,
        ObjectiveWithDestination.PRODUCT_CATALOG_SALES_X_UNDEFINED,
        ObjectiveWithDestination.CONVERSIONS_X_WEBSITE,
        ObjectiveWithDestination.LOCAL_AWARENESS_X_UNDEFINED,
        default_item=ObjectiveWithDestination.CONVERSIONS_X_WEBSITE,
    )

    contexts = Contexts.all_with_items(AWARENESS, CONSIDERATION, CONVERSIONS, APP_ACTIVITY, default_item=AWARENESS)


# TODO: find these in the SDK, they are from the online optimization goals docs
@cat_enum
class ObjectivePromotionTarget(Enum):
    UNDEFINED = Cat(None)
    INSTANT_EXPERIENCES_APP = Cat(None)
    MOBILE_APP = Cat(None)
    EVENT = Cat(None)
    PAGE_POST = Cat(None)


# https://developers.facebook.com/docs/marketing-api/bidding/guides/campaign-budget-optimization
# https://developers.facebook.com/docs/marketing-api/bidding/overview/bid-strategy

_bid_strategy = Campaign.BidStrategy


@cat_enum
class BidStrategy(Enum):
    COST_CAP = Cat(_bid_strategy.cost_cap)
    LOWEST_COST_WITHOUT_CAP = Cat(_bid_strategy.lowest_cost_without_cap, display_name="Lowest cost")
    LOWEST_COST_WITH_BID_CAP = Cat(_bid_strategy.lowest_cost_with_bid_cap)
    LOWEST_COST_WITH_MIN_ROAS = Cat("LOWEST_COST_WITH_MIN_ROAS")

    contexts = Contexts.all_with_items(LOWEST_COST_WITHOUT_CAP)


@cat_enum
class BudgetTimespan(Enum):
    DAILY = Cat(None)
    LIFETIME = Cat(None)
