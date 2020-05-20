import typing

from Core.Tools.Misc.EnumerationBase import EnumerationBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields


class ObjectiveToResultsFieldValueEnum(EnumerationBase):
    APP_INSTALLS = GraphAPIInsightsFields.mobile_app_install
    BRAND_AWARENESS = GraphAPIInsightsFields.estimated_ad_recallers
    CONVERSIONS = GraphAPIInsightsFields.conversions
    EVENT_RESPONSES = GraphAPIInsightsFields.event_responses
    LEAD_GENERATION = GraphAPIInsightsFields.leads
    LINK_CLICKS = GraphAPIInsightsFields.link_click
    MESSAGES = GraphAPIInsightsFields.messaging_conversation_started_7d
    PAGE_LIKES = GraphAPIInsightsFields.page_like
    POST_ENGAGEMENT = GraphAPIInsightsFields.post_engagement
    REACH = GraphAPIInsightsFields.reach
    VIDEO_VIEWS = GraphAPIInsightsFields.thru_plays
    PRODUCT_CATALOG_SALES = GraphAPIInsightsFields.product_catalog_sales


def map_objective_to_results_field_value(data: typing.Dict = None):
    objective = data.get(GraphAPIInsightsFields.objective, None)
    try:
        return ObjectiveToResultsFieldValueEnum.get_enum_by_name(objective).value
    except Exception as e:
        raise e
