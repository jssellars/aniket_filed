from datetime import datetime

from Tools.CaseConverter import CaseConverter
from Tools.ImportanceMapper import ImportanceMapper
from bson.objectid import ObjectId


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

    def __init__(self, originDict):
        self.__dict__ = self.convert_recommendation_to_camel_case(originDict)

    def convert_recommendation_to_camel_case(self, initialDict):
        camel_case_recommendation = {}
        for key in initialDict:
            if (isinstance(initialDict[key], ObjectId)):
                camel_case_recommendation['id'] = str((initialDict[key]))
                continue
            if (isinstance(initialDict[key], datetime)):
                camel_case_recommendation[CaseConverter.snake_to_camel_case(key)] = initialDict[key].isoformat()
                continue
            if (isinstance(initialDict[key], dict)):
                if (key=='application_details'):
                    camel_case_recommendation['applicationDetails'] = initialDict[key]
                    continue
                camel_case_recommendation[CaseConverter.snake_to_camel_case(key)] = self.convert_recommendation_to_camel_case(initialDict[key])
                continue
            if (isinstance(initialDict[key], list)):
                camel_case_recommendation[CaseConverter.snake_to_camel_case(key)] = [self.convert_recommendation_to_camel_case(item) for item in initialDict[key]]
                continue
            if (key == 'importance'):
                camel_case_recommendation[key] = ImportanceMapper.get_importance_string(initialDict[key])
                continue
            camel_case_recommendation[CaseConverter.snake_to_camel_case(key)] = initialDict[key]
        return camel_case_recommendation
