from marshmallow import fields

from Core.mapper import MappingBase


class AdsManagerUpdateStructureCommandMapping(MappingBase):
    client_manager_id = fields.String(required=True)
    client_customer_id = fields.String(required=True)
    campaign_id: fields.String()
    ad_group_id: fields.String()
    keyword_id: fields.String()
    edit_details: list


class QueryBuilderGoogleUpdateInfoMapping(MappingBase):
    field: fields.String(required=True)
    value: fields.Raw(required=True)
    campaign_id: fields.String()
    ad_group_id: fields.String()
    keyword_id: fields.String()
