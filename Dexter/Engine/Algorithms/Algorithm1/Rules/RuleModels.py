from enum import Enum
from Algorithms.Tools.ColumnsEnum import Metrics
from Infrastructure.Rabbit.Messages.RabbitMessagesMetadata import Recommendation
from Algorithms.Tools.Columns import RecommendationSources, ConfidenceImportanceValues


class MetricTrends(Enum):
    Increasing = 'Increasing'
    Decreasing = 'Decreasing'


class NonTrendAttributes(Enum):
    High = 'High'
    Low = 'Low'


industryStandards = {
    Metrics.Ctr.value: 0.90,
    Metrics.Frequency.value: 3.4,
    Metrics.Reach.value: 1000000.0,
    'RelevancyScore': 5.0
}


class Antecedent(object):
    metric = None
    attribute = None
    isTrend = None

    def __init__(self, metric, attribute, isTrend=True):
        self.metric = metric
        self.attribute = attribute
        self.isTrend = isTrend

    def evaluate(self, actor, mapper):
        mapped_metric = mapper[self.metric]
        if mapped_metric in actor:
            if self.isTrend:
                if actor[mapped_metric]['Angle'] > 0:
                    return self.attribute == MetricTrends.Increasing.value
                else:
                    return self.attribute == MetricTrends.Decreasing.value
            else:
                if self.attribute == NonTrendAttributes.High.value:
                    return actor[mapped_metric]['CurrentValue'] >= industryStandards.get(mapped_metric, 0)
                else:
                    return actor[mapped_metric]['CurrentValue'] < industryStandards.get(mapped_metric, 0)
        else:
            return False


class Rule(object):
    antecedents = None
    template = None
    recommendationType = None

    def __init__(self, antecedents, template, recommendationType):
        if isinstance(antecedents, list):
            self.antecedents = antecedents
        else:
            self.antecedents = [antecedents]
        self.template = template
        self.recommendationType = recommendationType

    def CheckApplication(self, actor, mapper):
        for antecedent in self.antecedents:
            if not antecedent.evaluate(actor, mapper):
                return False
        return True

    def GenerateRecommendation(self, level, id, ad_account_id, actor_data, confidence=ConfidenceImportanceValues.Medium.value,
                               importance=ConfidenceImportanceValues.Medium.value):
        # TODO: change the structure id
        recommendation = Recommendation()
        recommendation.structureId = str(id)
        recommendation.level = level
        recommendation.optimizationType = 'RuleBased'
        formattedTemplate = self.template.format(level=level)
        recommendation.template = formattedTemplate
        recommendation.recommendationType = self.recommendationType
        recommendation.source = RecommendationSources.Dexter.value
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
