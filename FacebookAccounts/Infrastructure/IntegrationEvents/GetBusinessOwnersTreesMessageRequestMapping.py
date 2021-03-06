from marshmallow import EXCLUDE

from Core.mapper import MapperBase, MapperNestedField
from FacebookAccounts.Infrastructure.IntegrationEvents.GetBusinessOwnersTreesMessageResponse import \
    BusinessOwner


class GetBusinessOwnersTreesMessageRequestMapping(MapperBase):
    business_owners = MapperNestedField(BusinessOwner, many=True)

    class Meta:
        unknown = EXCLUDE
