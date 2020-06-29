from Core.Tools.Misc.EnumerationBase import EnumerationBase


class RequestTypeEnum(EnumerationBase):
    BUSINESS_OWNER_UPDATE_EVENT = "BusinessOwnerPreferencesUpdatedEvent"
    BUSINESS_OWNER_CREATED_EVENT = "BusinessOwnerCreatedEvent"
    CAMPAIGN_CREATED_EVENT = "CampaignCreatedEvent"
