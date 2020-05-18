import itertools
import operator
import typing

from Potter.FacebookPixels.Infrastructure.Domain.FlatPixelStatsModel import FlatPixelStatsModel, PixelStatsRow
from Potter.FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIPixelStatsDto import GraphAPIPixelStatsDto


def flatten_pixel_stats(pixel_stats: typing.List[GraphAPIPixelStatsDto]) -> FlatPixelStatsModel:
    flat_pixel_stats = FlatPixelStatsModel()
    for stats in pixel_stats:
        for entry in stats.data:
            pixel_stats_row = PixelStatsRow(aggregation=stats.aggregation,
                                            start_time=stats.start_time,
                                            value=entry.value,
                                            count=entry.count)
            if flat_pixel_stats.stats:
                flat_pixel_stats.stats.append(pixel_stats_row)
            else:
                flat_pixel_stats.stats = [pixel_stats_row]

    return flat_pixel_stats


def group_pixel_stats_by_value(pixel_stats: typing.List[GraphAPIPixelStatsDto]) -> typing.Dict:
    flat_pixel_stats = flatten_pixel_stats(pixel_stats)
    get_attr_func = operator.attrgetter('value')
    grouped_pixel_stats = {k: list(g) for k, g in
                           itertools.groupby(sorted(flat_pixel_stats.stats, key=get_attr_func), get_attr_func)}

    return grouped_pixel_stats
