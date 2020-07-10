from marshmallow import EXCLUDE

from Core.Tools.Mapper.MapperBase import MapperBase, MapperNestedField
from Potter.FacebookAccounts.Infrastructure.IntegrationEvents.GetBusinessOwnersTreesMessageResponse import \
    BusinessOwner


class GetBusinessOwnersTreesMessageRequestMapping(MapperBase):
    business_owners = MapperNestedField(BusinessOwner, many=True)

    class Meta:
        unknown = EXCLUDE
