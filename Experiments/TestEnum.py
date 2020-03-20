from enum import Enum

class EnumerationBase(Enum):

    @classmethod
    def values(cls):
        return list(map(lambda v: v.value, cls))

    @classmethod
    def names(cls):
        return list(map(lambda v: v.name, cls))

    @classmethod
    def get_by_value(cls, value):
        match = next(filter(lambda x: x.value == value, cls))
        return match.name if match else None


class AdAccountField(EnumerationBase):
    NAME = "name"
    ACCOUNT_ID = "account_id"
    ID = "id"
    ACCOUNT_STATUS = "account_status"
    CURRENCY = "currency"
    BUSINESS = "business"


a = AdAccountField

print(hasattr(a, 'test'))
