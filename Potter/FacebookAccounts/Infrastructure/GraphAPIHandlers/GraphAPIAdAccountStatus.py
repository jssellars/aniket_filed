from Core.Tools.Misc.EnumerationBase import EnumerationBase


class GraphAPIAdAccountStatus(EnumerationBase):
    ACTIVE = 1
    DISABLED = 2
    UNSETTLED = 3
    PENDING_RISK_REVIEW = 7
    PENDING_SETTLEMENT = 8
    IN_GRACE_PERIOD = 9
    PENDING_CLOSURE = 100
    CLOSED = 101
    ANY_ACTIVE = 201
    ANY_CLOSED = 202