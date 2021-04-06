from difflib import SequenceMatcher
from enum import Enum

from Core.Tools.Misc.EnumerationBase import EnumerationBase


class State(Enum):
    INACTIVE = 0
    ACTIVE = 1
    REMOVED = 2


# Reference: https://developers.facebook.com/docs/facebook-pixel/reference#standard-events
class StandardEventType(EnumerationBase):
    ADD_PAYMENT_INFO = 1
    ADD_TO_CART = 2
    ADD_TO_WISHLIST = 3
    COMPLETE_REGISTRATION = 4
    CONTACT = 5
    CUSTOMIZE_PRODUCT = 6
    DONATE = 7
    FIND_LOCATION = 8
    INITIATE_CHECKOUT = 9
    LEAD = 10
    PAGE_VIEW = 11
    PURCHASE = 12
    SCHEDULE = 13
    SEARCH = 14
    START_TRIAL = 15
    SUBMIT_APPLICATION = 16
    SUBSCRIBE = 17
    VIEW_CONTENT = 18
    UNKNOWN = 19
    CUSTOM = 20


# Reference: https://developers.facebook.com/docs/marketing-api/reference/ad-promoted-object/v10.0
CUSTOM_EVENT_TYPE = {
    "RATE",
    "TUTORIAL_COMPLETION",
    "CONTACT",
    "CUSTOMIZE_PRODUCT",
    "DONATE",
    "FIND_LOCATION",
    "SCHEDULE",
    "START_TRIAL",
    "SUBMIT_APPLICATION",
    "SUBSCRIBE",
    "ADD_TO_CART",
    "ADD_TO_WISHLIST",
    "INITIATED_CHECKOUT",
    "ADD_PAYMENT_INFO",
    "PURCHASE",
    "LEAD",
    "COMPLETE_REGISTRATION",
    "CONTENT_VIEW",
    "SEARCH",
    "SERVICE_BOOKING_REQUEST",
    "MESSAGING_CONVERSATION_STARTED_7D",
    "LEVEL_ACHIEVED",
    "ACHIEVEMENT_UNLOCKED",
    "SPENT_CREDITS",
    "LISTING_INTERACTION",
    "D2_RETENTION",
    "D7_RETENTION",
    "OTHER",
}

# Create EventType dict with common types between standard and custom event types and similar names also mapped
standard = set(map(str.upper, StandardEventType.get_names()))
common_types = CUSTOM_EVENT_TYPE.intersection(standard)
common_types = dict(zip(common_types, common_types))

cet_only = list(CUSTOM_EVENT_TYPE.difference(common_types))
standard_only = list(set(standard).difference(common_types))

for word in cet_only:
    for s_word in standard_only:
        if SequenceMatcher(None, word, s_word).ratio() > 0.45:  # map closely similar names to single value
            common_types[s_word] = word
            common_types[word] = word
            standard_only.remove(s_word)

common_types.update(dict(zip(cet_only, cet_only)))  # add custom event types that are not part of the standard types
common_types.update(dict(zip(standard_only, standard_only)))  # add standard types that are not part of custom types

EventType = common_types
