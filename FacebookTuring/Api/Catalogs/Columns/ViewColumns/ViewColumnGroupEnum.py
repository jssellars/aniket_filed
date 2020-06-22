from enum import Enum


class ViewColumnGroupEnum(Enum):
    CLICKS = 'Clicks'
    PERFORMANCE = 'Performance'
    COST_PER_ACTION = 'Cost per action'
    COST_PER_UNIQUE_ACTION = 'Cost per unique action value'
    CONVERSION_VALUE = 'Conversion value'
    ENGAGEMENT = 'Engagement'
    VIDEOS = 'Videos'
    WEBSITES = 'Websites'
    OFFLINE = 'Offline'
    ONSITE_CONVERSIONS = 'Onsite conversions'
    APPS = 'Apps'
    EVENTS = 'Events'
    STANDARD_EVENTS = 'Standard events'
    STANDARD_EVENTS_COST_PER_CONVERSION = 'Standard events cost per conversion'
    UNIQUE_ACTIONS = 'Unique actions'
    CALCULATED_METRICS = 'Calculated metrics'
