from enum import Enum

from Core.Tools.Misc.EnumerationBase import EnumerationBase


class State(Enum):
    INACTIVE = 0
    ACTIVE = 1
    REMOVED = 2


class EventType(EnumerationBase):
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
