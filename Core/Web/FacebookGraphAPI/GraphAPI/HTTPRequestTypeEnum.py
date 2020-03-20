from enum import Enum


class HTTPRequestTypeEnum(Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'