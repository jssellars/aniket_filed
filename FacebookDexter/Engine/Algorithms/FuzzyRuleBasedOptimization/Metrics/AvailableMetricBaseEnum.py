from enum import Enum

from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.Infrastructure.Domain.Metrics.Metric import MetricBase


class AvailableMetricBaseEnum(Enum):
    RESULTS = MetricBase(FieldsMetadata.results.name, "Results")
    SPEND = MetricBase(FieldsMetadata.spend.name, "Amount spent")
    REACH = MetricBase(FieldsMetadata.reach.name, "Reach")
    LINK_CLICKS = MetricBase(FieldsMetadata.link_click.name, "Link clicks")
    PAGE_LIKES = MetricBase(FieldsMetadata.page_like.name, "Page likes")
    IMPRESSIONS = MetricBase(FieldsMetadata.impressions.name, "Impressions")
    PURCHASES = MetricBase(FieldsMetadata.purchases.name, "Purchases")
    VIDEO_PLAYS = MetricBase(FieldsMetadata.video_play.name, "Video plays")
    LEADS = MetricBase(FieldsMetadata.leads.name, "Leads")
    RSVPS = MetricBase(FieldsMetadata.event_responses.name, "RSVPs")
    APP_INSTALLS = MetricBase(FieldsMetadata.app_installs.name, "App installs")
    CONVERSIONS = MetricBase(FieldsMetadata.conversions.name, "Conversions")
    THRUPLAYS = MetricBase(FieldsMetadata.thruplay.name, "Thru plays")
    UNIQUE_CLICKS = MetricBase(FieldsMetadata.unique_click.name, "Unique clicks")
    POST_LIKES = MetricBase(FieldsMetadata.post_like.name, "Post likes")
    POST_COMMENTS = MetricBase(FieldsMetadata.post_comment.name, "Post comments")
    POST_SHARES = MetricBase(FieldsMetadata.post_share.name, "Post shares")
    POST_VIEWS = MetricBase(FieldsMetadata.post_views.name, "Post views")  #  todo: what are post views ??
    PURCHASES_VALUE = MetricBase(FieldsMetadata.purchases_value.name, "Purchases value")
    CLICKS = MetricBase(FieldsMetadata.all_clicks.name, "Clicks")
    OBJECTIVE = MetricBase(FieldsMetadata.objective.name, "Objective")
    RELEVANCY_SCORE = MetricBase(FieldsMetadata.relevancy_score.name, "Relevancy score")
    AUDIENCE_SIZE = MetricBase("audience_size", "Estimated audience size")
