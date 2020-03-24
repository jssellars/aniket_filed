from enum import Enum

from Algorithms.Tools.Columns import RecommendationSources, ConfidenceImportanceValues
from Algorithms.Tools.ColumnsEnum import Metrics
from Infrastructure.Rabbit.Messages.RabbitMessagesMetadata import Recommendation


class MetricTrends(Enum):
    INCREASING = 'Increasing'
    DECREASING = 'Decreasing'


class NonTrendAttributes(Enum):
    HIGH = 'High'
    LOW = 'Low'


industryStandards = {
    Metrics.CTR.value: 0.90,
    Metrics.FREQUENCY.value: 3.4,
    Metrics.REACH.value: 1000000.0,
    'RelevancyScore': 5.0
}


class Antecedent(object):
    metric = None
    attribute = None
    isTrend = None

    def __init__(self, metric, attribute, is_trend=True):
        self.metric = metric
        self.attribute = attribute
        self.isTrend = is_trend

    def evaluate(self, actor, mapper):
        mapped_metric = mapper[self.metric]
        if mapped_metric in actor:
            if self.isTrend:
                if actor[mapped_metric]['Angle'] > 0:
                    return self.attribute == MetricTrends.INCREASING.value
                else:
                    return self.attribute == MetricTrends.DECREASING.value
            else:
                if self.attribute == NonTrendAttributes.HIGH.value:
                    return actor[mapped_metric]['CurrentValue'] >= industryStandards.get(mapped_metric, 0)
                else:
                    return actor[mapped_metric]['CurrentValue'] < industryStandards.get(mapped_metric, 0)
        else:
            return False


class Rule(object):
    antecedents = None
    template = None
    recommendation_type = None

    def __init__(self, antecedents, template, recommendation_type):
        if isinstance(antecedents, list):
            self.antecedents = antecedents
        else:
            self.antecedents = [antecedents]
        self.template = template
        self.recommendation_type = recommendation_type

    def check_application(self, actor, mapper):
        for antecedent in self.antecedents:
            if antecedent.metric is None:
                print(antecedent.metric)
            if not antecedent.evaluate(actor, mapper):
                return False
        return True

    def generate_recommendation(self, level, structure_id, ad_account_id, actor_data,
                                confidence=ConfidenceImportanceValues.MEDIUM.value,
                                importance=ConfidenceImportanceValues.MEDIUM.value):
        # TODO: here, it should be snake_case, but for the writing in the DB
        # TODO: we will just keep it like this
        recommendation = Recommendation()
        recommendation.structureId = str(structure_id)
        recommendation.level = level
        recommendation.optimizationType = 'RuleBased'
        formatted_template = self.template.format(level=level)
        recommendation.template = formatted_template
        recommendation.recommendationType = self.recommendation_type
        recommendation.source = RecommendationSources.DEXTER.value
        recommendation.confidence = confidence
        recommendation.importance = importance
        recommendation.adAccountId = 'act_' + ad_account_id
        recommendation.metric = self.antecedents[0].metric
        # TODO: fill application details with useful info for Potter
        recommendation.applicationDetails = {}
        if level == 'campaign':
            recommendation.campaignId = actor_data['campaign_id']
            recommendation.parentId = actor_data['campaign_id']
            recommendation.structureName = actor_data['campaign_name']
            recommendation.campaignName = actor_data['campaign_name']
            recommendation.parentName = actor_data['campaign_name']
        elif level == 'adset':
            recommendation.campaignId = actor_data['campaign_id']
            recommendation.parentId = actor_data['campaign_id']
            recommendation.structureName = actor_data['adset_name']
            recommendation.campaignName = actor_data['campaign_name']
            recommendation.parentName = actor_data['campaign_name']
        elif level == 'ad':
            recommendation.campaignId = actor_data['campaign_id']
            recommendation.parentId = actor_data['adset_id']
            recommendation.structureName = actor_data['ad_name']
            recommendation.campaignName = actor_data['campaign_name']
            recommendation.parentName = actor_data['adset_name']
        return recommendation
