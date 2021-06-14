import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, ClassVar, Dict, List, Optional

from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendBuckets.BreakdownGroupedData import BreakdownGroupedData

logger = logging.getLogger(__name__)


class ApplyButtonType(Enum):
    DEFAULT = 0
    BEST_PERFORMING = 1
    CHOOSE_OTHER = 2
    NEW = 3


@dataclass
class ApplyParameters:
    business_owner_id: str
    budget_increase: Optional[float] = None
    budget_decrease: Optional[float] = None
    existing_breakdowns: Optional[List[BreakdownGroupedData]] = field(default_factory=dict)
    underperforming_breakdowns: Optional[List[str]] = None
    metric_name: Optional[str] = None
    no_of_days: Optional[int] = None


@dataclass
class RecommendationAction:
    config: Any
    fixtures: Any

    APPLY_TOOLTIP: ClassVar[str] = ""

    def process_action(self, recommendation: Dict, headers: str, apply_button_type: ApplyButtonType, command: Dict = None):
        raise NotImplementedError

    def get_action_parameters(self, apply_parameters: ApplyParameters, structure_details: Dict) -> Optional[Dict]:
        raise NotImplementedError

    @staticmethod
    def publish_response(response: Dict, fixtures: Any):
        rabbitmq_adapter = fixtures.rabbitmq_adapter
        rabbitmq_adapter.publish(response)
