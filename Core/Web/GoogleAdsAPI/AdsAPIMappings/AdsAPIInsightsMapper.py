import logging
import typing

from Core.Web.GoogleAdsAPI.Models.GoogleField import GoogleField
from Core.Web.GoogleAdsAPI.Models.GoogleFieldType import GoogleFieldType

logger = logging.getLogger(__name__)


class AdsAPIInsightsMapper:
    def map(self, requested_fields=None, response=None):
        if not response:
            return {}
        return self.map_response(requested_fields=requested_fields, data=response)

    @classmethod
    def map_response(cls, requested_fields: typing.List[GoogleField] = None, data: typing.List[typing.Dict] = None):
        mapped_response = {}
        for field in requested_fields:
            resource = field.resource_type if field.field_type == GoogleFieldType.ATTRIBUTE else field.field_type
            resource_level = getattr(data, resource.value)

            field_name = field.field_name.split(".")

            mapped_field_value = resource_level
            for attribute in field_name:
                mapped_field_value = cls.get_mapped_field(mapped_field_value, attribute)

            if field.conversion_function:
                mapped_field_value = field.conversion_function(mapped_field_value)

            mapped_response.update({field.name: mapped_field_value})

        return mapped_response

    @classmethod
    def get_mapped_field(cls, resource_level, attribute):
        try:
            return getattr(resource_level, attribute)
        except Exception as e:
            logger.exception(repr(e))
            return None
