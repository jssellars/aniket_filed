from Core.Tools.Misc.EnumerationBase import EnumerationBase


class GraphAPIBusinessRequestField(EnumerationBase):
    ID = "id"
    NAME = "name"


class GraphAPIAdAccountField(EnumerationBase):
    ID = "id"
    NAME = "name"
    ACCOUNT_ID = "account_id"
    ACCOUNT_STATUS = "account_status"
    CURRENCY = "currency"
    BUSINESS = "business"


class GraphAPIAssignedAdAccountField(EnumerationBase):
    ID = "id"
    ACCOUNT_ID = "account_id"
    NAME = "name"
    ACCOUNT_STATUS = "account_status"
    CURRENCY = "currency"
    BUSINESS = "business"
    BUSINESS_NAME = "business_name"
