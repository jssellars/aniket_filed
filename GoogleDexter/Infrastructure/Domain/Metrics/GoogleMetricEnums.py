import typing
from enum import Enum

import numpy as np

from Core.Dexter.Infrastructure.Domain.Metrics.MetricEnums import MetricTypeBaseEnum


class GoogleMetricTypeEnum(MetricTypeBaseEnum):
    INSIGHT = 1
    STRUCTURE = 2
    CREATIVE = 6  # not used
    INSIGHT_CATEGORICAL = 7
    PROSPECTING = 8  # not used
    KEYWORDS = 9


def count_distinct(values: typing.List[typing.Any]):
    return len(list(set(values)))


class AggregatorEnum(Enum):
    SUM = sum
    AVERAGE = np.mean
    LENGTH = len
    COUNT_DISTINCT = count_distinct
