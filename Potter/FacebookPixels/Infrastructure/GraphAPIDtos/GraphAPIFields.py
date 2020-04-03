from Core.Tools.Misc.EnumerationBase import EnumerationBase


class GraphAPIPixelFields(EnumerationBase):
    AUTOMATIC_MATCHING_FIELDS = 'automatic_matching_fields'
    CAN_PROXY = 'can_proxy'
    CODE = 'code'
    CREATION_TIME = 'creation_time'
    CREATOR = 'creator'
    DATA_USE_SETTING = 'data_use_setting'
    ENABLE_AUTOMATIC_MATCHING = 'enable_automatic_matching'
    FIRST_PARTY_COOKIE_STATUS = 'first_party_cookie_status'
    ID = 'id'
    IS_CREATED_BY_BUSINESS = 'is_created_by_business'
    IS_UNAVAILABLE = 'is_unavailable'
    LAST_FIRED_TIME = 'last_fired_time'
    NAME = 'name'
    OWNER_AD_ACCOUNT = 'owner_ad_account'
    OWNER_BUSINESS = 'owner_business'
    DOMAIN = 'domain'


class GraphAPIPixelCustomAudienceFields(EnumerationBase):
    ACCOUNT_ID = "account_id"
    ID = "id"
    NAME = "name"


class GraphAPIPixelDAChecksFields(EnumerationBase):
    ACTION_URI = "action_uri"
    DESCRIPTION = "description"
    KEY = "key"
    RESULT = "result"
    TITLE = "title"
    USER_MESSAGE = "user_message"


class GraphAPICustomConversionFields(EnumerationBase):
    ACCOUNT_ID = "account_id"
    AGGREGATION_RULE = "aggregation_rule"
    BUSINESS = "business"
    CREATION_TIME = "creation_time"
    CUSTOM_EVENT_TYPE = "custom_event_type"
    DATA_SOURCES = "data_sources"
    DEFAULT_CONVERSION_VALUE = "default_conversion_value"
    DESCRIPTION = "description"
    EVENT_SOURCE_TYPE = "event_source_type"
    FIRST_FIRED_TIME = "first_fired_time"
    ID = "id"
    IS_ARCHIVED = "is_archived"
    LAST_FIRED_TIME = "last_fired_time"
    IS_UNAVAILABLE = "is_unavailable"
    NAME = "name"
    RETENTION_DAYS = "retention_days"
    RULE = "rule"
    PIXEL = "pixel"


class GraphAPIPixelStatsFields(EnumerationBase):
    DATA = "data"
    START_TIME = "start_time"
    AGGREGATION = "aggregation"


class GraphAPICustomConversionStatsFields(EnumerationBase):
    DATA = "data"
    TIMESTAMP = "timestamp"
    AGGREGATION = "aggregation"
