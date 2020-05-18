import typing
from dataclasses import dataclass


@dataclass
class BusinessOwner:
    facebook_id: str = None


@dataclass
class GetBusinessOwnersTreesMessageRequest:
    message_type: str = "GetBusinessOwnersTreesMessageRequest"
    business_owners: typing.List[BusinessOwner] = None


"""
Sample request
{
  "business_owners": [
        {
          "facebook_id": "1623950661230875"
        },
        {
          "facebook_id": "1623950661230875"
        }
    ]
}

"""
