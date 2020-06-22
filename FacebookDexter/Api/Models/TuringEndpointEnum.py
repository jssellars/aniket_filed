from enum import Enum


class TuringEndpointEnum(Enum):
    DEV = "https://dev.api.facebook.turing.filed.com/api/v1/"
    DEV2 = "https://dev2-api-facebook-turing.filed.com/api/v1/"
    PROD = "https://prod-api-facebook-turing.filed.com/api/v1/"
    STAGING = "https://staging-api-facebook-turing.filed.com/api/v1/"
