import typing
from dataclasses import dataclass


@dataclass
class Customer:
    name: str = None
    id: int = None
    google_id: int = None


@dataclass
class GoogleUserPreferencesUpdatedEvent:
    google_id: str = None
    email_address: str = None
    refresh_token: str = None
    customers: typing.List[Customer] = None


"""
Sample request
{
  "google_id": "andrew@filed.com",
  "email_address": "andrew@filed.com",
  "refresh_token": "1//sh-sdgsd-NJk5i-dfhd",
  "customers": [
    {
      "name": "Filed",
      "id": 0,
      "google_id": 8503720627
    }
  ],
  "integration_event_id": "0d359d0d-18db-4b36-a8f0-06f78c7d51e3",
  "priority": 1,
  "creation_date": "2020-04-01T09:32:15.9784258Z",
  "auto_ack": false
}

"""
