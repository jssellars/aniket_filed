import typing

from marshmallow import EXCLUDE, INCLUDE, fields, post_load, pre_load

from Core.mapper import MapperBase
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
    ad_account_id = fields.String()
    campaigns = fields.List(fields.String)

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def build(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            data = object_to_json(data)

        return data

    @post_load
    def build(self, data: typing.Any, **kwargs):
        if self._target:
            return self._target(**data)

        return data
