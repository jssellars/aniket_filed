from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Optional, Union

from Core.mongo_adapter import MongoRepositoryBase
from FacebookDexter.Infrastructure.DexterRules.BreakdownAndAudiencesTemplates import (
    BreakdownRecommendationTemplate,
    AudienceRecommendationTemplate,
)
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendTemplates import (
    InfoRecommendationTemplate,
    RecommendationPriority,
)


@dataclass
class DexterOutput:
    analysis: str
    recommendation_template_key: str
    priority: RecommendationPriority
    title: str
    subtext: str
    quote: str

    RECOMMENDATION_ENTRY_MODEL: ClassVar[str] = "recommendation_entry_model"

    @classmethod
    def from_recommendation(
        cls, recommendation: Enum, trigger_variance: Optional[float] = None, no_of_days: Optional[int] = None
    ):
        raise NotImplementedError

    def process_output(self, output_repository: MongoRepositoryBase, **kwargs):
        raise NotImplementedError


@dataclass
class DexterRecommendationOutput(DexterOutput):
    trigger_variance: Optional[float] = None
    no_of_days: Optional[int] = None

    def process_output(self, output_repository: MongoRepositoryBase, **kwargs):
        output_repository.add_one(kwargs[self.RECOMMENDATION_ENTRY_MODEL])

    @classmethod
    def from_recommendation(
        cls, recommendation: Enum, trigger_variance: Optional[float] = None, no_of_days: Optional[int] = None
    ):
        analysis, priority, title, subtext, quote = recommendation.value
        template_name = recommendation.name
        return cls(analysis, template_name, priority, title, subtext, quote, trigger_variance, no_of_days)


def get_formatted_message(
    template: str,
    trigger_variance: Optional[float] = None,
    no_of_days: Optional[int] = None,
    breakdown_group: Optional[str] = None,
):
    if template in InfoRecommendationTemplate.__members__:
        output_enum = InfoRecommendationTemplate
    elif template in BreakdownRecommendationTemplate.__members__:
        output_enum = BreakdownRecommendationTemplate
    elif template in AudienceRecommendationTemplate.__members__:
        output_enum = AudienceRecommendationTemplate
    else:
        return

    if breakdown_group:
        breakdown_group = breakdown_group.replace(",", " -").replace("_", "-").title()

    return (
        output_enum[template]
        .value[0]
        .format(trigger_variance=trigger_variance, no_of_days=no_of_days, breakdown_group=breakdown_group)
    )


def get_output_enum(template: str):
    if template in InfoRecommendationTemplate.__members__:
        return InfoRecommendationTemplate

    elif template in BreakdownRecommendationTemplate.__members__:
        return BreakdownRecommendationTemplate

    elif template in AudienceRecommendationTemplate.__members__:
        return AudienceRecommendationTemplate

    return None
