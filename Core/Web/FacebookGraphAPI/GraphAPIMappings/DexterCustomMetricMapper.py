import itertools
import typing
from collections import ChainMap
from dataclasses import dataclass
from typing import Dict, Optional

from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldMapperBase import ActionFieldMapperBase
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FieldMapperResult import FieldMapperResult


class DexterCustomMetricMapper(ActionFieldMapperBase):

    def map(self, data: typing.Dict = None, field: typing.Any = None) -> typing.List[FieldMapperResult]:

        result = []
        for composed_field in field.composing_fields:
            result.append(composed_field.mapper.map(data, composed_field))

        mapped_data = [dict(ChainMap(*entry)) for entry in itertools.product(*result)][0]

        return [FieldMapperResult().set_field(field.name, CUSTOM_DEXTER_METRICS[field.name].calculate_cost(mapped_data))]


@dataclass
class CostPerMetric:
    numerator: str
    denominator: str
    multiplier: int = 1

    def calculate_cost(self, data: Dict) -> Optional[float]:
        try:
            if self.numerator in data and self.denominator in data:
                return data[self.numerator] * self.multiplier / data[self.denominator]
        except Exception as e:
            # Can consider logging but too many divisions by zero occur
            return


CUSTOM_DEXTER_METRICS = {
    "cost_per_result": CostPerMetric(
        numerator="amount_spent", denominator="results"
    ),
    "landing_page_conversion_rate": CostPerMetric(
        numerator="conversions", denominator="unique_clicks_all", multiplier=100
    ),
    "conversion_rate": CostPerMetric(
        numerator="purchases_total", denominator="clicks_all", multiplier=100
    ),
}
