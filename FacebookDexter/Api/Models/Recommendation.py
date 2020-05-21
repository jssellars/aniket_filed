from datetime import datetime
from bson.objectid import ObjectId
from Tools.ImportanceMapper import ImportanceMapper
from Tools.CaseConverter import CaseConverter

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

    def convert_recommendation_to_camel_case(self, originDict):
       camel_case_recommendation = {}
       for key in originDict:
            if (isinstance(originDict[key], ObjectId)):
                camel_case_recommendation['id'] = str((originDict[key]))
                continue
            if (isinstance(originDict[key], datetime)):
                camel_case_recommendation[CaseConverter.snake_to_camel_case(key)] = originDict[key].isoformat()
                continue
            if (isinstance(originDict[key], dict)):
                if (key=='application_details'):
                    camel_case_recommendation['applicationDetails'] = originDict[key]
                    continue
                camel_case_recommendation[CaseConverter.snake_to_camel_case(key)] = self.convert_recommendation_to_camel_case(originDict[key])
                continue
            if (isinstance(originDict[key], list)):                
                camel_case_recommendation[CaseConverter.snake_to_camel_case(key)] = [self.convert_recommendation_to_camel_case(item) for item in originDict[key]]
                continue
            if (key == 'importance'):
                camel_case_recommendation[key] = ImportanceMapper.get_importance_string(originDict[key])
                continue
            camel_case_recommendation[CaseConverter.snake_to_camel_case(key)] = originDict[key]
       return camel_case_recommendation