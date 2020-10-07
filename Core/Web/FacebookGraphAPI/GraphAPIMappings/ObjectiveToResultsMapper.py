import typing

from Core.Tools.Misc.EnumerationBase import EnumerationBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata


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
    if not objective:
        return ""
    results_field_value = ObjectiveToResultsFieldValueEnum.get_enum_by_name(objective)
    if results_field_value:
        return results_field_value.value
    else:
        return ""


class PixelCustomEventTypeToResult(EnumerationBase):
    ADD_TO_CART = FieldsMetadata.adds_to_cart_total
    CONTENT_VIEW = FieldsMetadata.content_views
    INITIATED_CHECKOUT = FieldsMetadata.checkouts_initiated_unique_total
    LEAD = FieldsMetadata.leads_total
    PURCHASE = FieldsMetadata.purchases_total


class PixelCustomEventTypeToCostPerResult(EnumerationBase):
    ADD_TO_CART = FieldsMetadata.adds_to_cart_cost
    CONTENT_VIEW = FieldsMetadata.content_views_cost
    INITIATED_CHECKOUT = FieldsMetadata.checkouts_initiated_unique_cost
    LEAD = FieldsMetadata.leads_cost
    PURCHASE = FieldsMetadata.purchases_cost


class AdSetOptimizationToResult(EnumerationBase):
    IMPRESSIONS = FieldsMetadata.impressions
    LEAD_GENERATION = FieldsMetadata.leads_total
    LINK_CLICKS = FieldsMetadata.link_clicks
    OFFSITE_CONVERSIONS = FieldsMetadata.other_offline_conversions_total
    PAGE_LIKES = FieldsMetadata.page_likes
    POST_ENGAGEMENT = FieldsMetadata.post_engagement
    REACH = FieldsMetadata.reach
    LANDING_PAGE_VIEWS = FieldsMetadata.landing_page_views_total
    THRUPLAY = FieldsMetadata.thru_plays


class AdSetOptimizationToCostPerResult(EnumerationBase):
    IMPRESSIONS = FieldsMetadata.cpm
    LEAD_GENERATION = FieldsMetadata.leads_cost
    LINK_CLICKS = FieldsMetadata.cost_per_link_click
    OFFSITE_CONVERSIONS = FieldsMetadata.other_offline_conversions_cost
    PAGE_LIKES = FieldsMetadata.cost_per_page_like
    POST_ENGAGEMENT = FieldsMetadata.cost_per_post_engagement
    REACH = FieldsMetadata.cost_per_1000_people_reached
    LANDING_PAGE_VIEWS = FieldsMetadata.landing_page_views_cost
    THRUPLAY = FieldsMetadata.cost_per_thru_play

