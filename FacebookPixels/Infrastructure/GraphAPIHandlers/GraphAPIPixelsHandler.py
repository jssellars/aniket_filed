import copy
import hashlib
import json
import typing
from datetime import datetime, timedelta

import humps
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adspixel import AdsPixel
from facebook_business.adobjects.adspixelstatsresult import AdsPixelStatsResult

from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from FacebookPixels.Infrastructure.Domain.Event import Event
from FacebookPixels.Infrastructure.Domain.Pixel import Pixel
from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPICustomConversionDto import GraphAPICustomConversionDto
from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIEnums import EventType, State
from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIFields import GraphAPICustomConversionFields
from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIFields import GraphAPIPixelCustomAudienceFields
from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIFields import GraphAPIPixelDAChecksFields
from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIFields import GraphAPIPixelFields
from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIFields import GraphAPIPixelStatsFields
from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIPixelCustomAudienceDto import \
    GraphAPIPixelCustomAudienceDto
from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIPixelDAChecksDto import GraphAPIPixelDAChecksDto
from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIPixelDto import GraphAPIPixelDto
from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIPixelStatsDto import GraphAPIPixelStatsDto
from FacebookPixels.Infrastructure.GraphAPIMappings.GraphAPICustomConversionMapping import \
    GraphAPICustomConversionMapping
from FacebookPixels.Infrastructure.GraphAPIMappings.GraphAPIMappingBase import \
    GraphAPIPixelCustomAudienceMapping, GraphAPIPixelDAChecksMapping
from FacebookPixels.Infrastructure.GraphAPIMappings.GraphAPIPixelMapping import GraphAPIPixelMapping
from FacebookPixels.Infrastructure.GraphAPIMappings.GraphAPIPixelStatsMapping import GraphAPIPixelStatsMapping
from FacebookPixels.Infrastructure.Tools.Misc import group_pixel_stats_by_value


class GraphAPIPixelHandler:
    __default_start_time = "1990-01-01"
    __facebook_datetime_format = "%Y-%m-%dT%H:%M:%S"
    __facebook_datetime_tz_separator = "+"

    @classmethod
    def get_pixels(cls,
                   permanent_token: typing.AnyStr = None,
                   account_id: typing.AnyStr = None,
                   config: typing.Any = None) -> typing.Tuple[typing.List[Pixel], typing.Any]:
        # initialize GraphAPI SDK
        _ = GraphAPISdkBase(config.facebook, permanent_token)

        # Get pixels for ad account
        pixel_mapper = GraphAPIPixelMapping(target=GraphAPIPixelDto)
        ad_account = AdAccount(fbid=account_id)
        pixels = ad_account.get_ads_pixels(fields=GraphAPIPixelFields.get_values())
        pixels = pixel_mapper.load(pixels, many=True)

        response = []
        errors = []
        for pixel in pixels:
            # Get custom audiences for current pixel
            try:
                custom_audiences = cls.__get_custom_audiences(ad_account, pixel.id)
            except Exception as e:
                custom_audiences = []
                errors.append(copy.deepcopy(Tools.create_error(e, code="IntegrationEventError")))

            # Get DA Checks for current pixel
            try:
                da_checks = cls.__get_da_checks(pixel.id)
            except Exception as e:
                da_checks = []
                errors.append(copy.deepcopy(Tools.create_error(e, code="IntegrationEventError")))

            # Get custom conversions for current pixel
            try:
                custom_conversions = cls.__get_custom_conversions(ad_account, pixel.id)
            except Exception as e:
                custom_conversions = []
                errors.append(copy.deepcopy(Tools.create_error(e, code="IntegrationEventError")))

            # Get stats for current pixel
            try:
                pixel_stats = cls.__get_pixel_stats(pixel.id)
            except Exception as e:
                pixel_stats = []
                errors.append(copy.deepcopy(Tools.create_error(e, code="IntegrationEventError")))

            # Assemble final pixels response
            pixel_dto = cls.__build_pixel(pixel, custom_audiences, da_checks, custom_conversions, pixel_stats, errors)

            response.append(pixel_dto)

        return response, errors

    @classmethod
    def __build_pixel(cls,
                      pixel: GraphAPIPixelDto = None,
                      custom_audiences: typing.List[GraphAPIPixelCustomAudienceDto] = None,
                      da_checks: typing.List[GraphAPIPixelDAChecksDto] = None,
                      custom_conversions: typing.List[GraphAPICustomConversionDto] = None,
                      pixel_stats: typing.List[GraphAPIPixelStatsDto] = None,
                      errors: typing.List[typing.Any] = None) -> Pixel:
        # todo: add pixel total count
        pixel_dto = Pixel()
        pixel_dto.details_as_json = object_to_json(pixel)
        try:
            pixel_dto.id = pixel.id
            pixel_dto.name = pixel.name
            pixel_dto.date_created = pixel.creation_time
            pixel_dto.last_updated = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            pixel_dto.domain = pixel.domain
            pixel_dto.creator = pixel.creator.name if pixel.creator else None
            pixel_dto.owner_business_name = pixel.owner_business.name if pixel.owner_business else None
            pixel_dto.audiences = custom_audiences
            pixel_dto.da_checks = da_checks
        except Exception as e:
            errors.append(copy.deepcopy(Tools.create_error(e, code="IntegrationEventError")))

        try:
            pixel_dto.events = [cls.__map_custom_conversion_to_event_model(custom_conversion, pixel.id) for
                                custom_conversion in custom_conversions]
        except Exception as e:
            errors.append(
                copy.deepcopy(Tools.create_error(e, code="IntegrationEventError")))

        try:
            if pixel_dto.events and pixel_stats:
                pixel_dto.events += cls.__map_pixel_stats_to_event_model(pixel_stats, pixel.id)
            elif pixel_stats:
                pixel_dto.events = cls.__map_pixel_stats_to_event_model(pixel_stats, pixel.id)
        except Exception as e:
            errors.append(
                copy.deepcopy(Tools.create_error(e, code="IntegrationEventError")))

        pixel_dto.state = cls.__is_pixel_active(pixel_dto)

        return pixel_dto

    @staticmethod
    def __is_pixel_active(pixel_dto: Pixel = None, is_unavailable: bool = None) -> int:
        pixel_state = is_unavailable if is_unavailable else len(pixel_dto.events) > 0
        return int(pixel_state)

    @staticmethod
    def __create_hash_id(pixel_id: typing.AnyStr = None,
                         event_name: typing.AnyStr = None,
                         event_type: typing.AnyStr = None):

        if not event_name:
            event_name = "Unknown"

        name_string = pixel_id + event_name + str(event_type)
        return hashlib.sha1(name_string.encode('utf-8')).hexdigest()

    @classmethod
    def __map_custom_conversion_to_event_model(cls, custom_conversion: GraphAPICustomConversionDto = None,
                                               pixel_id: typing.AnyStr = None) -> Event:
        event = Event()
        event.id = custom_conversion.id if custom_conversion.id else cls.__create_hash_id(pixel_id,
                                                                                          custom_conversion.name,
                                                                                          EventType.CUSTOM.value)
        event.name = custom_conversion.name
        event.date_created = custom_conversion.creation_time
        event.last_updated = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        event.event_type = EventType.CUSTOM.value
        event.details_as_json = object_to_json(custom_conversion)
        event.state = int(not custom_conversion.is_unavailable)
        event.event_activity = custom_conversion.last_fired_time
        event.custom_event_type = custom_conversion.custom_event_type if custom_conversion.custom_event_type else None
        event.rule_as_json = json.loads(custom_conversion.rule) if custom_conversion.rule else None

        return event

    @classmethod
    def __map_pixel_stats_to_event_model(cls, pixel_stats: typing.List[GraphAPIPixelStatsDto],
                                         pixel_id: typing.AnyStr = None) -> typing.List[Event]:
        grouped_pixel_stats = group_pixel_stats_by_value(pixel_stats)
        events = []
        for event_type, event_stats in grouped_pixel_stats.items():
            event_type_name = humps.depascalize(event_type)
            event_type_enum = EventType.get_by_name(event_type_name.lower())

            if event_type_enum:
                event = Event()
                event.name = event_type
                event.event_type = event_type_enum
                event.id = cls.__create_hash_id(pixel_id, event_type, event_type_enum)
                event.event_activity = max([row.start_time for row in event_stats])
                event.event_count = sum([row.count for row in event_stats])
                event.last_updated = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                event.custom_event_type = (event_type_name.upper()
                                           if event_type_enum != EventType.UNKNOWN.value else None)

                last_week = datetime.now() - timedelta(days=7)
                event_last_fired_time = datetime.strptime(
                    event.event_activity.split(cls.__facebook_datetime_tz_separator)[0],
                    cls.__facebook_datetime_format)
                if event_last_fired_time >= last_week:
                    event.state = State.ACTIVE.value
                else:
                    event.state = State.INACTIVE.value

                events.append(event)

        return events

    @staticmethod
    def __build_custom_audience_params(pixel_id: typing.AnyStr) -> typing.MutableMapping:
        return {"pixel_id": pixel_id}

    @classmethod
    def __get_custom_audiences(cls,
                               ad_account: AdAccount = None,
                               pixel_id: typing.AnyStr = None) -> typing.List[GraphAPIPixelCustomAudienceDto]:
        custom_audience_mapper = GraphAPIPixelCustomAudienceMapping(target=GraphAPIPixelCustomAudienceDto)
        custom_audiences = ad_account.get_custom_audiences(fields=GraphAPIPixelCustomAudienceFields.get_values(),
                                                           params=cls.__build_custom_audience_params(pixel_id))
        custom_audiences = custom_audience_mapper.load(custom_audiences, many=True)
        return custom_audiences

    @classmethod
    def __get_da_checks(cls, pixel_id: typing.AnyStr = None) -> typing.List[GraphAPIPixelDAChecksDto]:
        dachecks_mapper = GraphAPIPixelDAChecksMapping(target=GraphAPIPixelDAChecksDto)
        da_checks = AdsPixel(fbid=pixel_id).get_da_checks(fields=GraphAPIPixelDAChecksFields.get_values())
        da_checks = dachecks_mapper.load(da_checks, many=True)
        return da_checks

    @staticmethod
    def __filter_custom_conversion_by_pixel_id(custom_conversions: typing.List[GraphAPICustomConversionDto] = None,
                                               pixel_id: typing.AnyStr = None) -> typing.List[
        GraphAPICustomConversionDto]:
        filtered_custom_conversions = [custom_conversion for custom_conversion in custom_conversions
                                       if custom_conversion.pixel_id == pixel_id]
        return filtered_custom_conversions

    @classmethod
    def __get_custom_conversions(cls,
                                 ad_account: AdAccount = None,
                                 pixel_id: typing.AnyStr = None) -> typing.List[GraphAPICustomConversionDto]:
        custom_conversion_mapper = GraphAPICustomConversionMapping(target=GraphAPICustomConversionDto)
        custom_conversions = ad_account.get_custom_conversions(fields=GraphAPICustomConversionFields.get_values())
        custom_conversions = custom_conversion_mapper.load(custom_conversions, many=True)
        custom_conversions = cls.__filter_custom_conversion_by_pixel_id(custom_conversions, pixel_id)
        return custom_conversions

    @classmethod
    def __build_pixel_stats_params(cls):
        return {
            "aggregation": AdsPixelStatsResult.Aggregation.event,
            "start_time": cls.__default_start_time
        }

    @classmethod
    def __get_pixel_stats(cls,
                          pixel_id: typing.AnyStr = None) -> typing.List[GraphAPIPixelStatsDto]:
        pixel_stats_mapper = GraphAPIPixelStatsMapping(target=GraphAPIPixelStatsDto)
        pixel_stats = AdsPixel(fbid=pixel_id).get_stats(fields=GraphAPIPixelStatsFields.get_values(),
                                                        params=cls.__build_pixel_stats_params())
        pixel_stats = pixel_stats_mapper.load(pixel_stats, many=True)
        return pixel_stats
