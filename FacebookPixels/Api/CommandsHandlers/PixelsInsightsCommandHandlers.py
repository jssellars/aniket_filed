import typing

from Core.Tools.Misc.ObjectSerializers import object_to_json
from FacebookPixels.Api.Commands.PixelsInsightsCommand import PixelsInsightsCommand
from FacebookPixels.Api.Dtos.PixelsInsightsResponseDto import PixelsInsightsResponseDto
from FacebookPixels.Api.Mappings.LevelToGraphAPIPixelsInsightsHandler import \
    LevelToGraphAPIPixelsInsightsHandler
from FacebookPixels.Api.Mappings.PixelsInsightsLevel import PixelsInsightsLevel
from FacebookPixels.Api.Mappings.PixelsInsightsResponseDtoMapping import PixelsInsightsResponseDtoMapping
from FacebookPixels.Api.startup import config, fixtures
from FacebookPixels.Infrastructure.Tools.Misc import flatten_pixel_stats


class PixelsInsightsCommandHandler:

    @classmethod
    def handle(cls, command: PixelsInsightsCommand) -> typing.List[PixelsInsightsResponseDto]:
        pixels_insights_level = PixelsInsightsLevel.get_by_value(command.level)
        graph_api_handler = LevelToGraphAPIPixelsInsightsHandler.get_enum_by_name(pixels_insights_level).value

        params = object_to_json(command)
        insights = graph_api_handler.handle(config=config, fixtures=fixtures, **params)
        insights = flatten_pixel_stats(insights)
        response_mapper = PixelsInsightsResponseDtoMapping(target=PixelsInsightsResponseDto)

        response = response_mapper.load(insights.stats, many=True)

        return response
