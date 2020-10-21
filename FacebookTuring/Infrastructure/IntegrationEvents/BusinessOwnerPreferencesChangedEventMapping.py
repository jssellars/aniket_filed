from marshmallow import EXCLUDE, fields

from Core.Tools.Mapper.MapperBase import MapperBase, MapperNestedField
from FacebookTuring.Infrastructure.IntegrationEvents.BusinessOwnerPreferencesChangedEvent import BusinessOwnerStatus, \
    AdAccountDetails, BusinessDetails


class BusinessOwnerPreferencesChangedEventMapping(MapperBase):
    user_filed_id = fields.Integer()
    id = fields.String()
    user_type = fields.String()
    status = MapperNestedField(target=BusinessOwnerStatus)
    ad_accounts = MapperNestedField(target=AdAccountDetails, many=True)
    businesses = MapperNestedField(target=BusinessDetails, many=True)

    class Meta:
        unknown = EXCLUDE
