from datetime import datetime

from bson.objectid import ObjectId

from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationKeysSnakeCase, \
    RecommendationKeysCamelCase

class CaseConverter:
    @staticmethod
    def snake_to_camel_case(text):
        components = text.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

class ImportanceMapper:

    @staticmethod
    def get_importance_string(confidence):
        if (confidence == 1):
            return 'LOW'
        if (confidence == 2):
            return 'MEDIUM'
        if (confidence == 3):
            return 'HIGH'

    @staticmethod
    def get_importance_value(confidence):
        if (confidence == 'LOW'):
            return 1
        if (confidence == 'MEDIUM'):
            return 2
        if (confidence == 'HIGH'):
            return 3


# todo: reinspect this, it has some imports frm facebook dexter
class Recommendation(object):
    id = None
    actionBreakdown = None
    structureId = None
    level = None
    optimizationType = None
    recommendationType = None
    confidence = None
    importance = None
    source = None
    campaignId = None
    parentId = None
    adAccountId = None
    createdAt = None
    category = None
    template = None
    metric = None
    applicationDetails = None
    applicationDate = None
    channel = None
    parentName = None
    campaignName = None
    structureName = None
    breakdown = None

    def __init__(self, origin_dict):
        self.__dict__ = self.convert_recommendation_to_camel_case(origin_dict)

    def convert_recommendation_to_camel_case(self, origin_dict):
        camel_case_recommendation = {}
        for key in origin_dict:
            if isinstance(origin_dict[key], ObjectId):
                camel_case_recommendation[RecommendationKeysCamelCase.ID.value] = str((origin_dict[key]))
                continue
            if isinstance(origin_dict[key], datetime):
                camel_case_recommendation[CaseConverter.snake_to_camel_case(key)] = origin_dict[key].isoformat()
                continue
            if isinstance(origin_dict[key], dict):
                if key == RecommendationKeysSnakeCase.APPLICATION_DETAILS.value:
                    camel_case_recommendation[RecommendationKeysCamelCase.APPLICATION_DETIALS.value] = origin_dict[key]
                    continue
                camel_case_recommendation[
                    CaseConverter.snake_to_camel_case(key)] = self.convert_recommendation_to_camel_case(
                    origin_dict[key])
                continue
            if isinstance(origin_dict[key], list):
                camel_case_recommendation[CaseConverter.snake_to_camel_case(key)] = [
                    self.convert_recommendation_to_camel_case(item) for item in origin_dict[key]]
                continue
            if key == RecommendationKeysSnakeCase.IMPORTANCE.value:
                camel_case_recommendation[key] = ImportanceMapper.get_importance_string(origin_dict[key])
                continue
            camel_case_recommendation[CaseConverter.snake_to_camel_case(key)] = origin_dict[key]
        return camel_case_recommendation
