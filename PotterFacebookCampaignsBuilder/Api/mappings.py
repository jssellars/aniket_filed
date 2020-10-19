import typing

from marshmallow import EXCLUDE, INCLUDE, fields, post_load, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Tools.Misc.ObjectSerializers import object_to_json


class AdPreviewCommand(MapperBase):
    class Meta:
        unknown = INCLUDE

    @post_load
    def build(self, data: typing.Any, **kwargs):
        mapped_data = dict(
            business_owner_id=data.get("business_owner_facebook_id"),
            account_id=data.get("ad_account_id"),
            page_facebook_id=data.get("page_id"),
            instagram_facebook_id=data.get("instagram_id"),
            ad_template=data.get("advert"),
        )
        if mapped_data["ad_template"]:
            mapped_data["ad_format"] = mapped_data["ad_template"]["device_placement_position"]["facebook_key"]

        if self._target:
            return self._target(**mapped_data)

        return mapped_data


class PublishCampaignResponseDto(MapperBase):
    business_owner_facebook_id = fields.String()
    campaign_goal = fields.String()
    ad_account_id = fields.String()
    use_dexter_optimization = fields.Boolean()
    # campaign_template_filed_id = fields.String()
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

        data["use_dexter_optimization"] = data["campaign_optimization_details"]["dexter_optimization"][
            "use_dexter_optimization"
        ]
        data["campaign_template_filed_id"] = data["campaign_template"]["campaign_template_filed_id"]
        data["average_conversion_value"] = data["campaign_optimization_details"]["dexter_optimization"][
            "average_conversion_value"
        ]
        return data

    @post_load
    def build(self, data: typing.Any, **kwargs):
        if self._target:
            return self._target(**data)

        return data
