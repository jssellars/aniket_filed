import typing

from Core.mapper import MapperBase
from marshmallow import EXCLUDE, INCLUDE, fields, post_load


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
            objective=data.get("objective")
        )
        if mapped_data["ad_template"]:
            mapped_data["ad_format"] = mapped_data["ad_template"]["device_placement_position"]["facebook_key"]

        if self._target:
            return self._target(**mapped_data)

        return mapped_data


class SmartCreatePublishRequest(MapperBase):
    user_filed_id = fields.Int()
    business_owner_facebook_id = fields.String()
    ad_account_id = fields.String()
    template_id = fields.Int()
    step_one_details = fields.Dict()
    step_two_details = fields.Dict()
    step_three_details = fields.Dict()
    step_four_details = fields.Dict()

    class Meta:
        unknown = EXCLUDE


class SmartEditPublishRequest(MapperBase):
    user_filed_id = fields.Int()
    business_owner_facebook_id = fields.String()
    ad_account_id = fields.String()
    campaigns = fields.List(fields.Dict())
    adsets = fields.List(fields.Dict())
    ads = fields.List(fields.Dict())

    class Meta:
        unknown = EXCLUDE


class AddAdsetAdPublishRequest(MapperBase):
    user_filed_id = fields.Int()
    business_owner_facebook_id = fields.String()
    ad_account_id = fields.String()
    parent_level = fields.String()
    child_level = fields.String()
    parent_ids = fields.List(fields.String())
    child_ids = fields.List(fields.String())
    adsets = fields.List(fields.Dict())
    ads = fields.List(fields.Dict())

    class Meta:
        unknown = EXCLUDE
