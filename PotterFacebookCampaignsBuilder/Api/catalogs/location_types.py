from facebook_business.adobjects.adplacepageset import AdPlacePageSet

from PotterFacebookCampaignsBuilder.Api.catalogs.base import Base
from PotterFacebookCampaignsBuilder.Api.catalogs.node import Node

# https://developers.facebook.com/docs/marketing-api/audiences/reference/basic-targeting
#
# recent: People whose recent location is selected area, as determined from mobile device data.
#   Not available to exclud locations.
# home: People whose stated location in Facebook profile “current city” is in an area.
#   Facebook validates this by IP and information from their friends’ profile locations.
# travel_in: People whose most recent location is selected area.
#   Determined by mobile device data, and more than 100 miles from stated
#   current city in their Facebook profile. Not available to exclude locations.
#
# If no location_types, defaults to ['home'].
# You cannot use travel_in with other values in location_types.
# To target “people living in or recently in this location”, add both recent and home in location_types.

_location_types = AdPlacePageSet.LocationTypes

home = Node(_location_types.home)
recent = Node(_location_types.recent)
travel_in = Node("travel_in")


class LocationTypes(Base):
    living_in_or_recently_in = Node("LIVING_IN_OR_RECENTLY_IN", home, recent)
    living_in = Node("LIVING_IN", home)
    recently_in = Node("RECENTLY_IN", recent)
    traveling_in = Node("TRAVELING_IN", travel_in)
