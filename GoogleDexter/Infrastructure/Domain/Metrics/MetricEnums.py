import typing
from enum import Enum

import numpy as np


class MetricTypeEnum(Enum):
    INSIGHT = 1
    STRUCTURE = 2
    AUDIENCE = 3  # not used
    INTERESTS = 4  # not used
    PIXEL = 5  # not used
    CREATIVE = 6  # not used
    INSIGHT_CATEGORICAL = 7
    PROSPECTING = 8  # not used
    KEYWORDS = 9


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
