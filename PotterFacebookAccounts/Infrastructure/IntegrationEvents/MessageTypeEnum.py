from Core.Tools.Misc.EnumerationBase import EnumerationBase


class RequestTypeEnum(EnumerationBase):
    BUSINESS_OWNER_UPDATE_REQUEST = "GetBusinessOwnersTreesMessageRequest"
    BUSINESS_OWNER_ACCOUNT_SPEND_REQUEST = "GetAdAccountsAmountSpentInsightMessageRequest"


class ResponseTypeEnum(EnumerationBase):
    BUSINESS_OWNER_UPDATE_REQUEST = "GetBusinessOwnersTreesMessageResponse"
    BUSINESS_OWNER_ACCOUNT_SPEND_REQUEST = "GetAdAccountsAmountSpentInsightMessageResponse"
