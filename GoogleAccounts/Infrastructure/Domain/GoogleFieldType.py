from enum import Enum


class GoogleFieldType(Enum):
    ATTRIBUTE = "attribute"
    SEGMENT = "segments"
    METRIC = "metrics"


class GoogleResourceType(Enum):
    CUSTOMER = "customer"
    CUSTOMER_CLIENT = "customer_client"
