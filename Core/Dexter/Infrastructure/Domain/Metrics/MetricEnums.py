import typing
from enum import Enum

import numpy as np

class MetricTypeBaseEnum(Enum):
    pass

class MetricTrendTimeBucketEnum(Enum):
    ONE_DAY = 1
    THREE_DAYS = 3
    SEVEN_DAYS = 7
    FOURTEEN_DAYS = 14
    THIRTY_DAYS = 30
    SIXTY_DAYS = 60
    NINETY_DAYS = 90


def count_distinct(values: typing.List[typing.Any]):
    return len(list(set(values)))


class AggregatorEnum(Enum):
    SUM = sum
    AVERAGE = np.mean
    LENGTH = len
    COUNT_DISTINCT = count_distinct
    STANDARD_DEVIATION = np.std
