from enum import Enum


class RecommendationField(Enum):
    OBJECT_ID = '_id'
    STRUCTURE_ID = 'structure_id'
    LEVEL = 'level'
    OPTIMIZATION_TYPE = 'optimization_type'
    RECOMMENDATION_TYPE = 'recommendation_type'
    CONFIDENCE = 'confidence'
    IMPORTANCE = 'importance'
    SOURCE = 'source'
    CAMPAIGN_ID = 'campaign_id'
    PARENT_ID = 'parent_id'
    AD_ACCOUNT_ID = 'ad_account_id'
    CREATED_AT = 'created_at'
    CATEGORY = 'category'
    TEMPLATE = 'template'
    METRIC = 'metric'
    APPLICATION_DETAILS = 'application_details'
    APPLICATION_DATE = 'applicationDate'
    CHANNEL = 'channel'
    PARENT_NAME = 'parent_name'
    CAMPAIGN_NAME = 'campaign_name'
    STRUCTURE_NAME = 'structure_name'
    BREAKDOWN = 'breakdown'
    STATUS = 'status'
    APPLIED_BY = 'applied_by'

