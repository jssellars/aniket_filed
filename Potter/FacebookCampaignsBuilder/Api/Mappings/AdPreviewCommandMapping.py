import typing

from marshmallow import post_load, INCLUDE

from Core.Tools.Mapper.MapperBase import MapperBase


class AdPreviewCommandMapping(MapperBase):
    class Meta:
        unknown = INCLUDE

    @post_load
    def build(self, data: typing.Any, **kwargs):
        mapped_data = {}
        # Extract data from request
        mapped_data['business_owner_id'] = data.get('business_owner_facebook_id')
        mapped_data['account_id'] = data.get('ad_account_id')
        mapped_data['page_facebook_id'] = data.get('page_id')
        mapped_data['instagram_facebook_id'] = data.get('instagram_id')
        mapped_data['ad_template'] = data.get('advert')
        if mapped_data['ad_template']:
            mapped_data['ad_format'] = mapped_data['ad_template']['device_placement_position']['facebook_key']

        if self._target:
            return self._target(**mapped_data)
        else:
            return mapped_data
