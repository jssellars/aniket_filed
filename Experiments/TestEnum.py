import itertools
import operator
from itertools import groupby
from operator import itemgetter

from Potter.FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIPixelStatsDto import GraphAPIPixelStatsDto, GraphAPIPixelStatsDataDto
from Potter.FacebookPixels.Infrastructure.Tools.Misc import flatten_pixel_stats

l = [
    GraphAPIPixelStatsDto(aggregation="event", start_time="2020-03-24T00:00:00+0200", data=[GraphAPIPixelStatsDataDto(value="PageView", count=10),
                                                                                            GraphAPIPixelStatsDataDto(value="Subscribe", count=10)]),
    GraphAPIPixelStatsDto(aggregation="event", start_time="2020-03-23T00:00:00+0200", data=[GraphAPIPixelStatsDataDto(value="PageView", count=10),
                                                                                            GraphAPIPixelStatsDataDto(value="Subscribe", count=10)]),
    GraphAPIPixelStatsDto(aggregation="event", start_time="2020-03-22T00:00:00+0200", data=[GraphAPIPixelStatsDataDto(value="PageView", count=10)])
]

f = flatten_pixel_stats(l)

get_attr_func = operator.attrgetter('value')
grouped_pixel_stats = {k: list(g) for k, g in itertools.groupby(sorted(f.stats, key=get_attr_func), get_attr_func)}

print(f)
