from enum import Enum

from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport

from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum, Contexts

# TODO: add documentation link(s)

_platform = ContentDeliveryReport.Platform


@cat_enum
class Platform(Enum):
    AUDIENCE_NETWORK = Cat(_platform.audience_network, display_name="Apps & Sites")
    FACEBOOK = Cat(_platform.facebook)
    INSTAGRAM = Cat(_platform.instagram)
    MESSENGER = Cat(_platform.messenger)
    WHATSAPP = Cat(_platform.whatsapp)

    contexts = Contexts.all_with_items(FACEBOOK, INSTAGRAM, AUDIENCE_NETWORK, default_item=FACEBOOK)


# TODO: add documentation link(s)

_position = ContentDeliveryReport.Position


@cat_enum
class Position(Enum):
    ALL_PLACEMENTS = Cat(_position.all_placements)  # TODO: see if it makes sense to keep
    AN_CLASSIC = Cat(_position.an_classic, display_name="Audience Network Native")
    FACEBOOK_GROUPS_FEED = Cat(_position.facebook_groups_feed)
    FACEBOOK_STORIES = Cat(_position.facebook_stories)
    FEED = Cat(_position.feed)
    GROUPS = Cat(_position.groups)
    HIDDEN_AAA = Cat(_position.hidden_aaa)  # TODO: see if it makes sense to keep
    INSTAGRAM_EXPLORE = Cat(_position.instagram_explore)
    INSTAGRAM_IGTV = Cat(_position.instagram_igtv)
    INSTAGRAM_STORIES = Cat(_position.instagram_stories)
    INSTANT_ARTICLE = Cat(_position.instant_article)
    INSTREAM_VIDEO = Cat(_position.instream_video)
    JOBS_BROWSER = Cat(_position.jobs_browser)
    MARKETPLACE = Cat(_position.marketplace)
    MESSENGER_INBOX = Cat(_position.messenger_inbox)
    MESSENGER_STORIES = Cat(_position.messenger_stories)
    OTHERS = Cat(_position.others)
    REWARDED_VIDEO = Cat(_position.rewarded_video)
    RIGHT_HAND_COLUMN = Cat(_position.right_hand_column)
    SEARCH = Cat(_position.search)
    STATUS = Cat(_position.status)
    SUGGESTED_VIDEO = Cat(_position.suggested_video)
    VIDEO_FEEDS = Cat(_position.video_feeds)


@cat_enum
class Placement(Enum):
    FACEBOOK_FEED = Cat(None, Platform.FACEBOOK, Position.FEED)
    FACEBOOK_RIGHT_COLUMN = Cat(None, Platform.FACEBOOK, Position.RIGHT_HAND_COLUMN)
    FACEBOOK_INSTANT_ARTICLES = Cat(None, Platform.FACEBOOK, Position.INSTANT_ARTICLE)
    FACEBOOK_IN_STREAM_VIDEO = Cat(None, Platform.FACEBOOK, Position.INSTREAM_VIDEO)
    FACEBOOK_MARKETPLACE = Cat(None, Platform.FACEBOOK, Position.MARKETPLACE)
    FACEBOOK_STORIES = Cat(None, Platform.FACEBOOK, Position.FACEBOOK_STORIES)
    FACEBOOK_SEARCH_RESULTS = Cat(None, Platform.FACEBOOK, Position.SEARCH)
    FACEBOOK_VIDEO_FEEDS = Cat(None, Platform.FACEBOOK, Position.VIDEO_FEEDS)
    INSTAGRAM_STORIES = Cat(None, Platform.INSTAGRAM, Position.INSTAGRAM_STORIES)
    INSTAGRAM_FEED = Cat(None, Platform.INSTAGRAM, Position.FEED)
    INSTAGRAM_EXPLORE = Cat(None, Platform.INSTAGRAM, Position.INSTAGRAM_EXPLORE)
    # TODO: the categories are AN NATIVE + BANNER + INTERSTITIAL, the last two aren't represented
    AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL = Cat(None, Platform.AUDIENCE_NETWORK, Position.AN_CLASSIC)
    AUDIENCE_NETWORK_REWARDED_VIDEO = Cat(None, Platform.AUDIENCE_NETWORK, Position.REWARDED_VIDEO)
    SPONSORED_MESSAGE = Cat(None)  # TODO: find mapping to Platform and Position
    MESSENGER_INBOX = Cat(None, Platform.MESSENGER, Position.MESSENGER_INBOX)
    MESSENGER_STORIES = Cat(None, Platform.MESSENGER, Position.MESSENGER_STORIES)
    # TODO: 'INSTREAM_VIDEO', displayName: 'Audience Network In-stream video', imageName: 'audience-network-in-stream'

    joint_fields = [Platform, Position]
