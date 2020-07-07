from datetime import datetime
from bson.objectid import ObjectId
from FacebookDexter.Api.Tools.ImportanceMapper import ImportanceMapper
from FacebookDexter.Api.Tools.CaseConverter import CaseConverter


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
                camel_case_recommendation['id'] = str((origin_dict[key]))
                continue
            if isinstance(origin_dict[key], datetime):
                camel_case_recommendation[CaseConverter.snake_to_camel_case(key)] = origin_dict[key].isoformat()
                continue
            if isinstance(origin_dict[key], dict):
                if key == 'application_details':
                    camel_case_recommendation['applicationDetails'] = origin_dict[key]
                    continue
                camel_case_recommendation[
                    CaseConverter.snake_to_camel_case(key)] = self.convert_recommendation_to_camel_case(origin_dict[key])
                continue
            if isinstance(origin_dict[key], list):
                camel_case_recommendation[CaseConverter.snake_to_camel_case(key)] = [
                    self.convert_recommendation_to_camel_case(item) for item in origin_dict[key]]
                continue
            if key == 'importance':
                camel_case_recommendation[key] = ImportanceMapper.get_importance_string(origin_dict[key])
                continue
            camel_case_recommendation[CaseConverter.snake_to_camel_case(key)] = origin_dict[key]
        return camel_case_recommendation
