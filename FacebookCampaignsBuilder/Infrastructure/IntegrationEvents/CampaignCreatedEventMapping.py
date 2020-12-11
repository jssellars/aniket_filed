import typing

from marshmallow import EXCLUDE, fields, pre_load

from Core.mapper import MapperNestedField, MapperBase
from FacebookCampaignsBuilder.Infrastructure.IntegrationEvents.CampaignCreatedEvent import CampaignTree


class CampaignCreatedEventMapping(MapperBase):
    business_owner_id = fields.String()
    account_id = fields.String()
    campaign_tree = MapperNestedField(target=CampaignTree, many=True)

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if isinstance(data, list):
            data = {
                'campaign_tree': data
            }
        return data

    class Meta:
        unknown = EXCLUDE
