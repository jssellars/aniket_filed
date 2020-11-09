from enum import Enum

from facebook_business.adobjects.adplacepageset import AdPlacePageSet

from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum

# https://developers.facebook.com/docs/marketing-api/audiences/reference/basic-targeting#available-fields-2
# location_types
#   recent: People whose recent location is selected area, as determined from mobile device data.
#     Not available to exclud locations.
#   home: People whose stated location in Facebook profile “current city” is in an area.
#     Facebook validates this by IP and information from their friends’ profile locations.
#   travel_in: People whose most recent location is selected area.
#     Determined by mobile device data, and more than 100 miles from stated
#     current city in their Facebook profile. Not available to exclude locations.
#
# If no location_types, defaults to ['home'].
# You cannot use travel_in with other values in location_types.
# To target “people living in or recently in this location”, add both recent and home in location_types.

_location_types = AdPlacePageSet.LocationTypes


@cat_enum
class LocationType(Enum):
    HOME = Cat(_location_types.home)
    RECENT = Cat(_location_types.recent)

    TRAVEL_IN = Cat("travel_in")


@cat_enum
class LocationTypeGroup(Enum):
    LIVING_IN_OR_RECENTLY_IN = Cat(None, LocationType.HOME, LocationType.RECENT)
    LIVING_IN = Cat(None, LocationType.HOME)
    RECENTLY_IN = Cat(None, LocationType.RECENT)
    TRAVELING_IN = Cat(None, LocationType.TRAVEL_IN)
