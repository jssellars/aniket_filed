import typing

from Core.Tools.Misc.ObjectSerializers import object_to_json
from PotterFacebookPixels.Api.Commands.PixelsInsightsCommand import PixelsInsightsCommand
from PotterFacebookPixels.Api.Dtos.PixelsInsightsResponseDto import PixelsInsightsResponseDto
from PotterFacebookPixels.Api.Mappings.LevelToGraphAPIPixelsInsightsHandler import \
    LevelToGraphAPIPixelsInsightsHandler
from PotterFacebookPixels.Api.Mappings.PixelsInsightsLevel import PixelsInsightsLevel
from PotterFacebookPixels.Api.Mappings.PixelsInsightsResponseDtoMapping import PixelsInsightsResponseDtoMapping
from PotterFacebookPixels.Api.Startup import startup
from PotterFacebookPixels.Infrastructure.Tools.Misc import flatten_pixel_stats


class PixelsInsightsCommandHandler:

    @classmethod
    def handle(cls, command: PixelsInsightsCommand) -> typing.List[PixelsInsightsResponseDto]:
        pixels_insights_level = PixelsInsightsLevel.get_by_value(command.level)
        graph_api_handler = LevelToGraphAPIPixelsInsightsHandler.get_enum_by_name(pixels_insights_level).value

        params = object_to_json(command)
        insights = graph_api_handler.handle(startup=startup, **params)
        insights = flatten_pixel_stats(insights)
        response_mapper = PixelsInsightsResponseDtoMapping(target=PixelsInsightsResponseDto)

        response = response_mapper.load(insights.stats, many=True)

        return response
