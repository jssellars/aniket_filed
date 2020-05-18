import typing

from marshmallow import EXCLUDE, fields, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Tools.Misc.ObjectSerializers import object_to_json


class PublishCampaignResponseDtoMapping(MapperBase):
    business_owner_facebook_id = fields.String()
    campaign_goal = fields.String()
    ad_account_id = fields.String()
    use_dexter_optimization = fields.Boolean()
    campaign_template_filed_id = fields.String()
    user_filed_id = fields.Integer()
    average_conversion_value = fields.Float()
    campaigns = fields.List(fields.String)
    errors = fields.List(fields.Dict)

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def build(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            data = object_to_json(data)

        data['use_dexter_optimization'] = data['campaign_optimization_details']['dexter_optimization'][
            'use_dexter_optimization']
        data['campaign_template_filed_id'] = data['campaign_template']['campaign_template_filed_id']
        data['average_conversion_value'] = data['campaign_optimization_details']['dexter_optimization'][
            'average_conversion_value']
        return data
