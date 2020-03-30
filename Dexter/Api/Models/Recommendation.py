from datetime import datetime
from bson.objectid import ObjectId
from Tools.ConfidenceImportanceMapper import ConfidenceImportanceMapper

class Recommendation(object):
    id = None
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
    template = None
    metric = None
    applicationDetails = None
    channel = None
    parentName = None
    campaignName = None
    structureName = None



    def __init__(self, originDict):

        for key in originDict:
            if (isinstance(originDict[key], datetime)):
                self.__dict__[key] = originDict[key].isoformat()
                continue
            if (isinstance(originDict[key], ObjectId)):
                self.__dict__['id'] = str((originDict[key]))
                continue
            if (key in ['confidence', 'importance']):
                self.__dict__[key] = ConfidenceImportanceMapper.get_confidence_importance_string(originDict[key])
                continue
            self.__dict__[key] = originDict[key]
