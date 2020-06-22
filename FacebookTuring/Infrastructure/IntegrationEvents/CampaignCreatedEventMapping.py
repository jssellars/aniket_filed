from marshmallow import EXCLUDE, fields

from Core.Tools.Mapper.MapperBase import MapperNestedField, MapperBase
from FacebookTuring.Infrastructure.IntegrationEvents.CampaignCreatedEvent import CampaignTree


class CampaignCreatedEventMapping(MapperBase):
    business_owner_id = fields.String()
    campaign_tree = MapperNestedField(target=CampaignTree, many=True)

    class Meta:
        unknown = EXCLUDE
