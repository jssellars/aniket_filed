from enum import Enum


class Costs(Enum):
    CPC = 'Cpc'
    CPM = 'Cpm'
    CPP = 'Cpp'


class Metrics(Enum):
    SPEND = 'Spend'
    REACH = 'Reach'
    CLICKS = 'Clicks'
    IMPRESSIONS = 'Impressions'
    CTR = 'Ctr'
    ROAS = 'Roas'
    FREQUENCY = 'Frequency'
    RELEVANCY_SCORE = 'RelevancyScore'  # Not used


class GroupBy(Enum):
    ID = 'FiledId'
    BREAKDOWN_VALUE = 'Parameters_DeliveryBreakdownValue'
    DATE = 'Parameters_Until'
    FACEBOOK_ID = 'FacebookId'
    AD_ACCOUNT_ID = 'account_id'
    # Goal = 'Goal'


class Where(Enum):
    DATE_START = "date_start"
    DATE_STOP = "date_stop"
    DATE = 'Parameters_Until'
    BREAKDOWN_NAME = 'BreakdownName'
    AD_ACCOUNT_ID = 'AdAccountId'
    BREAKDOWN_ID = 'Parameters_DeliveryBreakdownId'
    ACTION_BREAKDOWN_ID = 'Parameters_ActionBreakdownId'
